#!/usr/bin/env python3

###############################################################################
#
# Copyright (c) 2025, Anders Andersen, UiT The Arctic University of
# Norway. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# - Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# - Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
###############################################################################

R"""A Python module for generating Python module documentation

The `pypimdoc` module generates documentation for a Python program or
module based on a README template file and the Python source code with
its documentation text strings.  The README template is a Markdown document
with the addition of what we call *module documentation methods*, or
just *MD-methods* for short.  These methods are on separate lines
inside HTML comments:

```
<!-- doc(PyPiMDoc.process_template, hlevel=2) -->
```

In the example above, the MD-method line will be replaced by the
documentation string of `process_template` method of the `PyPiMDoc` class
with a level 2 heading.

"""


#
# Some useful values
#

# Current version of module
version = "0"


#
# Import Python modules used
#

# Import standard modules
import sys, re
import urllib.parse
import importlib.util
from pathlib import Path
from io import TextIOBase
from inspect import signature, getdoc, isclass, ismethod, isfunction, ismodule
from collections.abc import Callable

# Use subprocess to perform the command line operations
import subprocess

# Import some `pygments` stuff
#from pygments import highlight
#from pygments.lexers.python import PythonLexer
from pygments.util import ClassNotFound
from pygments.styles import get_style_by_name
#from pygments.formatters import HtmlFormatter, LatexFormatter


#
# Regular expressions used by the module
#

# Match `pypimdoc` MD-methods in README templates, like the line
# `doc(PyPiMDoc,hlevel=1,complete=True)`
_mdmethod = re.compile(r"^(?P<method>\w+)\((?P<args>.*)\)\s*$")
_mdmethod_complete = re.compile(
    r"^<!--\s*(?P<method>\w+)\((?P<args>.*)\)\s*-->\s*$")
_mdmethod_begin = re.compile(
    r"^<!--\s*(?P<method>\w+)\((?P<args>.*)\)\s*$")
_mdmethod_end = re.compile(
    r"^\s*-->\s*$")
_md_name_arg = re.compile(r"[\w \t='\"]*name=(?P<name>['\"]\w+['\"]).*")

# Match <class>.<method>, like `PyPiMDoc.process_template`
_cmnames = re.compile(r"(?P<class>\w+)\.(?P<method>\w+)")

# Match module file name <name>.py, like `pypimdoc.py`
_pysrcname = re.compile(r"^(?P<name>\w+)\.(?P<ext>py)$")

# Match a header (empty line followed by title ending with colon
# followed by empty line)
_margsheader = re.compile(r'\n\s*\n([\w /]+:)\n\s*\n')

# In-line code starts and ends with lines starting with three single
# back-quotes
_inlinecode = re.compile(r'^```')

# Matches for the `help2md` function (sol = start of line)
_sol_lc = re.compile(r"^[a-z].*")
_sol_usage = re.compile(r"^Usage:")
_sol_ws_rest = re.compile(r"^ +.*$")
_sol_empty = re.compile(r"^$")
_sol_descr = re.compile(r"^[a-zA-Z_0-9][a-zA-Z_0-9 ]+.*[^:]$")
_sol_args = re.compile(r"^[OP][a-zA-Z_0-9 ]+:$")
_py_fn = re.compile(r"[a-z]+[.]py")
_single_quoted = re.compile(r"'[^']+'")
_sol_ten_ws = re.compile(r"^          ")
_cont_line = re.compile(r"` \| ")
_sol_two_ws = re.compile(r"^  ")


#
# Help functions
#

def help2md(help_msg: str) -> str:
    R"""Convert a help message to markdown

    Convert a help message (the output from a command when the `-h`
    flag is given) to a valid and well-formated markdown text.

    The function is inspired by the awk script
    [`help2md`](https://github.com/valeriangalliat/help2md) and my own
    version of this awk script updated to better match the help
    message generated by the `argparse` module:
    `help2md-argparse.awk`.

    Arguments/return value:

    `help_msg`: The help message to convert

    `returns`: The markdown text

    """

    # Initialize some variables
    usage: bool = False
    descr: bool = False
    options: bool = False
    prev: str = ""
    nr: int = 0
    md_txt: str = ""

    # Parse each line of `help_msg`
    for line in help_msg.splitlines():

        # Count lines
        nr += 1

        # Use `match` if matching the beginning of line, and `search`
        # to match inside line

        # Uppercase first character in paragraphs
        # /^[a-z]/ 
        if _sol_lc.match(line):
            line = line[0].upper() + line[1:]

        # Initialize usage section (and optional first usage line)
        # /^Usage:/
        if _sol_usage.match(line):
            usage = True
            line = re.sub(r"^Usage: +", "\n```bash\n", line)
            line = re.sub(r"^Usage:$", "\n```bash", line)
            utxt = "\n**Usage:**\n" + line
            continue

        # Format usage code
        # usage && /^ +.*$/
        if usage and _sol_ws_rest.match(line):
            line = re.sub(r"^ +", " ", line)
            utxt += line
            continue

        # Close usage code if after usage
        # usage && /^$/
        if usage and _sol_empty.match(line):
            usage = False
            descr = True
            utxt += "\n```"
            continue

        # Close options
        # options && /^$/
        if options and _sol_empty.match(line):
            options = False

        # Description? (if so, first text after usage)
        # descr && /^[a-zA-Z_0-9][a-zA-Z_0-9 ]+.*[^:]$/
        if descr and _sol_descr.match(line):
            descr = False
            prev = "*" + line + "*"
            line = utxt

        # Initialize options/positional-arguments section
        # !usage && /^[OP][a-zA-Z_0-9 ]+:$/
        if (not usage) and _sol_args.match(line):
            if descr: descr = False
            options = True
            line = "**" + line + "**\n\nName | Description\n---- | -----------"

        # Remove .py from command
        # /[a-z]+[.]py/
        if _py_fn.search(line):
            line = re.sub(r"[.]py", "", line)

        # Substitute quote with backquote
        # /'[^']+'/
        if _single_quoted.search(line):
            line = line.replace("'", "`", 2)

        # Join continuation lines with previous line
        # /^          /
        if _sol_ten_ws.match(line):

            # options && (prev !~ /` \| /)
            if options and not _cont_line.search(prev):
                line = re.sub(r"^ *", "` | ", line)
            else:
                line = re.sub(r"^ *", " ", line)
            prev += line
            continue

        # Format arguments/options table
        # !usage && /^  /
        if not usage and _sol_two_ws.match(line):
            line = re.sub(r"^  +", "`", line)
            line = re.sub(r"  +", "` | ", line)

        # Initialize buffered line
        # NR == 1
        if nr == 1:
            prev = line

        # Print line (one line buffered)
        # NR > 1 
        else:
            md_txt += prev + "\n"
            prev = line

    # END
    md_txt += prev + "\n"
    return md_txt


def _get_nested_attr(ns, attr_str: str) -> object:
    R"""Get a nested attribute

    Return the named nested attribute `attr_str` from the namespace
    `ns`.  For example, if `attr_str` is `"a.b"`, return the attribute
    `b` of `a`.

    Arguments/return value:

    `ns`: Name space to find nested attribute in

    `attr_str`: Nested attributed as a string using dot notation

    `returns`: The attribute named in `attr_str`

    """
    attr = ns
    nested_attr = attr_str.split(".")
    for a in nested_attr:
        attr = getattr(attr, a)
    return attr

def _mkid(txt: str, idlist: list, max_length: int = 20) -> str:
    R"""Make a valid id or reference

    Create a valid and unique HTML id/reference from the text string
    `txt`.  The text string is tyically a title or a Python object
    name.

    Arguments/return value:

    `txt`: The text to be transformed to an id

    `idlist`: A list of used ids

    `max_length`: The maximum length of the id

    `returns`: The new unique id

    """

    # Create a quoted (safe) id and start with that one as the new id
    qid = urllib.parse.quote_plus(txt[:max_length])
    nid = qid
    lqid = len(qid)

    # Continue until we have a unique id
    i = 1
    while nid in idlist:

        # Count and create a numer to append (to ensure uniqueness) 
        num = str(i)

        # Ensure that the id is not longer than `max_length`
        newl = lqid + len(num)
        if newl > max_length:
            rl = newl - max_length
            nid = qid[:-rl] + num
        else:
            nid = qid + num

        # Increase counter
        i += 1

    # Add new unique id to id list and return the new id
    idlist.append(nid)
    return nid

def _ismethod(attr: object) -> bool:
    R"""A more relaxed implementation of `ismethod`

    This version of `ismethod` will also return `True` if it is not in
    an instance of the class of the method. The trick (that might give
    false positives) is to check that the function's long name
    (`__qualname__`) is a nested name (with a dot).

    Arguments/return value:

    `attr`: The object we are verifying is a method

    `returns`: `True` if `attr` is a method

    """
    if ismethod(attr) or isfunction(attr):
        cmmatch = _cmnames.match(attr.__qualname__)
        if cmmatch:
            return True
    return False

def _getdoc(attr: object) -> str:
    R"""Extended get documentation of attribute

    This extended `getdoc` function will first try to return the
    documentation string of the attribute, and if that is not
    available, the related (possibly multiline) comment.

    Arguments/return value:

    `attr`: The object to get the doc string from

    `returns`: The documentation string

    """
    doc = getdoc(attr)
    if not doc:
        try:
            doc = getcomments(attr)
        except:
            doc = None
    if not doc:
        if hasattr(attr, "__name__"):
            m = f" from {attr.__name__}"
        else:
            m = ""
        raise PyPiMDocError(f"Unable to get documentation string (or comment){m}")
    return doc

def _signature(attr: object) -> str | None:
    R"""Get signature of function or method as a text string

    Returns the signature of a function or method. If it is a method,
    `self` is removed from the signature. If it is not a function or
    method, `None` is returned.

    Arguments/return value:

    `attr`: The object to get the signature of

    `returns`: The signature of the function or method as a text
    string, or `None` if `attr` is not a function or a method

    """
    if isfunction(attr):
        sig = str(signature(attr))
        if _ismethod(attr):
            if "(self, " in sig:
                sig = sig.replace("self, ", "", 1)
            elif "(self)" in sig:
                sig = sig.replace("self", "", 1)
        return sig
    return None

def _special_first_line(doc: str) -> tuple:
    R"""If first line is special, split it from the documentation string
    
    The first line is special if it is a single line of text followed
    by an empty line.

    Arguments/return value:

    `doc`: A documentation string

    `returns`: If the firt line is special, the first line and the
    rest of the documentation string, otherwise `None` and the unchanged
    documentation string

    """
    doclist = doc.splitlines()
    if (len(doclist) > 1 and (firstline:=doclist[0].strip())
        and (doclist[1].strip() == "")):
        doc = "\n".join(doclist[1:]).strip()
    else:
        firstline = None
    return firstline, doc


#
# Exceptions/errors by the module
#

class PyPiMDocError(Exception):
    R"""Any error in the `pypimdoc` module"""
    def __init__(self, errmsg: str):
        self.errmsg = errmsg


#
# The main class of the module
#

class PyPiMDoc:
    R"""The Python module documentation class

    A module implementing the different MD-methods used in the
    markdown template for the documentation of the Python program or
    module. Currently the following MD-methods are implemented:

    - `h`: Insert a heading 

    - `doc`: Insert the documentation for the given object (module,
      function, class, method)

    - `bdoc`: Insert the documentation for the objects (module,
      function, class, method) listed from here to the next MD-method
      `edoc`

    - `edoc`: End the list of objects to document

    - `toc`: Insert a table of contents with all items following this
      (see also `btoc` and `etoc` below, but in the general use case
      they are not needed).

    - `btoc`: Alternative start to register items (headings) for
      table of contents (if the `toc` command does not start it)

    - `etoc`: End register items (headings) for table of contents (if
      it should stop before end of document)

    - `eval`: Insert the text output of the Python code evaluated in
      the name space of the module and the MD-methods' local name
      space

    - `code`: Execute the code to populate the MD-methods' local name
      space

    - `bcode`: Execute the code between this MD-method and the next
      MD-method `ecode`

    - `ecode`: End the code to be executed
    
    - `cmd`: Insert the text output of the (shell) command

    - `cmd_cb`: Insert the text output of the (shell) command in a
      code block

    - `help`: Insert the output from a help command reformatted as
      markdown

    """
    

    def __init__(
            self,
            filename: str,
            name: str = "",
            base_heading_level: int = 1,
            toc_begin: int = 1,
            toc_end: int = 3):
        R"""Initialize a Python module documentation object

        Initialize a Python module documentation object, including
        loading the Python module (Python source code) and prepare the
        document generation.

        Arguments:

        `filename`: The file name of the module to document

        `name`: The name of the module (default generated from the
        `filename`)

        `base_heading_level`: All generated headings are at this level
        or above (default 1)
        
        `toc_begin`: Include items in table of contents from this
        level (relative to `base_heading_level`, default 1)

        `toc_end`: Include items in table of contents to this level
        (relative to `base_heading_level`, default 2)

        """

        # Initiate object values from the constructor arguments (or defaults)
        self.filename = filename
        self.name = name
        self.base_heading_level = base_heading_level
        self.toc_begin = base_heading_level + toc_begin - 1
        self.toc_end = base_heading_level + toc_end - 1

        # The documentation can contain a set of table of contents
        self.mktoc = set()

        # Save toc items here (for each toc set)
        self.tocpart = {}

        # Save arguments from MD-method `bdoc` here, and as a
        # consequence show that we are between a `bdoc` and an `edoc`
        # MD-method in the README template
        self.bdoc = ()

        # Save the objects between a `bdoc` and an `edoc` MD-method in
        # the README template here
        self.objlist = []

        # Save the code between a `bcode` and an `ecode` MD-method
        # here, and as a consequence show that we are between a
        # `bcode` and an `ecode` MD-method in the README template
        self.code = ""

        # A list of used ids (to ensure the we generate unique ids)
        self.idlist = []

        # The matching method of "bdoc" or "bcode ("edoc" or "ecode")
        self.md_end = None

        # How different level of headers are created (pre, post), 0
        # means no header
        self.hmarkers = [
            ("", ""),		# 0
            ("# ", ""),		# 1
            ("## ", ""),	# 2
            ("### ", ""),	# 3
            ("#### ", ""),	# 4
            ("**", "**"),	# 5
            ("*", "*")]		# > 5

        # Name of the module to document (either given or from the file name)
        if not self.name:
            mpn = _pysrcname.match(self.filename)
            if mpn:
                self.name = mpn["name"]
            else:
                raise PyPiMDocError(
                    f"Unable to determine module: {self.filename}")

        # Load the module to document
        spec = importlib.util.spec_from_file_location(self.name, self.filename)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

        # Make namespaces used by the MD-methods
        self.mgns = vars(self.module)
        self.mlns = {"args_kw": lambda *args, **kw: (args, kw)}

        # The firstline and the rest of the module documentation string
        if "__doc__" in self.mgns and self.mgns["__doc__"]:
            mdoc_list = self.mgns["__doc__"].splitlines()
            self.mgns["mdoc_firstline"] = mdoc_list[0]
            self.mgns["mdoc_body"] = "\n".join(mdoc_list[1:]).strip()


        # List all MD-methods (from this class starting with "_md_")
        self.md_methods = _list_md_methods(
            self, rm_pre = True, qualname = False, sort_order = None)


    def _get_real_hlevel(self, hlevel: int) -> int:
        R"""Calibrate levels with the base heading level

        Calibrate all references to heading levels by added the base
        headings level to the given heading level (except when the
        given heading level is zero).

        Arguments/return value:

        `hlevel`: The given heading level

        `returns`: The calibrated (adjusted) heading level

        """
        if hlevel > 0:
            hlevel +=  self.base_heading_level - 1
        return hlevel

    
    def _mk_h(
            self,
            title: str,
            hlevel: int,
            hid: str = "",
            no_toc: bool = False) -> str:
        R"""Create a heading and add it to the table of contents

        Create a heading at the given level `hlevel` with the given
        title. If a table of contents is generated, add an id to the
        title and add an entry to the table of contents.

        Arguments/return value:

        `title`: The title (text) of the heading (section)

        `hlevel`: The heading level, where 1 is the highest level

        `hid`: Optional heading id that might be modified to ensure
        uniqueness (if not given, it will generated if needed)

        `no_toc`: If `True` do not add to table of contents
        (default `False`)

        `returns`: A heading typeset to the correct heading level

        """

        # Create `hid` if not given
        if not no_toc:
            if hid:
                hid = _mkid(hid, self.idlist)
            else:
                hid = _mkid(title, self.idlist)

        # Create header markers
        hlevelpre, hlevelpost = self.hmarkers[hlevel]
            
        # Add to table of content
        if not no_toc:
            if (self.mktoc and hlevel >= self.toc_begin
                and hlevel <= self.toc_end):
                for t in self.mktoc:
                    ilevel = hlevel - self.toc_begin
                    self.tocpart[t]["items"].append({
                        "ilevel": ilevel,
                        "content": f'<a href="#{hid}">{title}</a>'})
                    
        # Create and return header
        if hid:
            idtxt = f'<a id="{hid}"></a>'
        else:
            idtxt = ""
        return f'\n{hlevelpre}{idtxt}{title}{hlevelpost}\n'

    
    def process_template(self, template: TextIOBase) -> str:
        R"""Read and process template

        The template file is the driver of the document generation. In
        its simplest form, the template is a markdown document that
        becomes the module documentation. The template includes some
        special commands (MD-methods) used to fetch documentation from
        the module (including the documentation strings in the
        module).

        Arguments/return value:

        `template`: The README template file

        `returns`: The processed markdown README file content

        """

        # Start with empty README file content
        mdoc = ""

        # We are not in inline code mode in the beginning
        inline = False

        # Go through each line
        for line in template:

            # Is this inline code?
            icode = _inlinecode.match(line)
            if icode:
                if inline:
                    inline = False
                else:
                    inline = True
                mdoc += line
                continue
            elif inline:
                mdoc += line
                continue

            # Is this a command?
            if (mcmd := _mdmethod_begin.match(line)):
                if mcmd["method"] in ["bdoc", "btoc", "bcode"]:
                    self.md_end = "e" + mcmd["method"][1:]
                    if mcmd["method"] == "btoc":
                        m = _md_name_arg.match(mcmd["args"])
                        if m:
                            name_arg = m["name"]
                        else:
                            name_arg = '"toc"'
                        self.md_end_args = f"name = {name_arg}"
                    else:
                        self.md_end_args = ""
                else:
                    raise PyPiMDocError(
                        f'Unexpected MD-method: {mcmd["method"]} ' + \
                        '(does not support MD-method block)')
            elif self.md_end:
                if _mdmethod_end.match(line):
                    mcmd = {"method": self.md_end, "args": self.md_end_args}
                    self.md_end = None
                elif self.md_end in ["edoc", "etoc"]:
                    mcmd = _mdmethod.match(line)
            else:
                mcmd = _mdmethod_complete.match(line)
                

            # Yes, a command
            if mcmd:

                # Process the found MD-method
                res = self.process_method(mcmd["method"], mcmd["args"])

            # No
            else:
                res = line
            
            # Code?
            if self.code and res:
                self.code += res
                
            # The special case between MD-methods `bdoc` and `edoc`
            elif self.bdoc and res:

                # A list (maybe returned from the MD-method `eval`)
                if type(res) is list:
                    self.objlist += res

                # A string
                else:

                    # Remove surounding spaces/newlines
                    res = res.strip()

                    # Add text to object list (if it is not an emprty line)
                    if res:
                        self.objlist += res

            # The normal case
            elif res:
                mdoc += res

        # Add toc
        if self.tocpart:

            # Go through every toc (we can have more than one)
            for t in self.tocpart:

                # Might need this to adjust indent
                min_i = min([i["ilevel"] for i in self.tocpart[t]["items"]])

                # For each text item in the current toc
                toc = []

                # Each toc text item starts with this
                start = self.tocpart[t]["toc_item_start"]

                # Each item in the toc
                for item in self.tocpart[t]["items"]:

                    # Calculate the indent size and make the indentation
                    indentsize = \
                        self.tocpart[t]["toc_item_indent"] * \
                        (item["ilevel"] - min_i)
                    indent = " " * indentsize

                    # Add the text item 
                    toc.append(f'{indent}{start}{item["content"]}')

                # Insert the toc in the documentation string
                mdoc = mdoc.replace(
                    f"%({t})s",
                    self.tocpart[t]["toc_item_end"].join(toc))

        # Return doc
        return mdoc

    
    def process_method(self, method_name: str, args_str: str) -> str:
        R"""Process a MD-method

        Process a MD-method with the given name and arguments.

        Arguments/return value:

        `method_name`: MD-method name

        `args_str`: the arguments to the MD-method as a string

        `returns`: returns the documentation part generated by the MD-method

        """

        # Get MD-method
        full_name = "_md_" + method_name
        if method_name in self.md_methods and hasattr(self, full_name):
            method = getattr(self, full_name)
        else:
            raise PyPiMDocError(f"Unknown MD-method: {method_name}")

        # Get the arguments
        args, kw = eval(
            f"args_kw({args_str})",
            globals=self.mgns, locals=self.mlns)

        # Perform the method
        return method(*args, **kw)

    
    def _md_h(self, title: str, hlevel: int, 
              hid: str = "", no_toc: bool = False) -> str:
        R"""Insert a heading

        Insert a heading at the given level (including adjustment
        from base level).

        Arguments/return value:

        `title`: A title

        `hlevel`: The heading level for the title

        `hid`: An id for the title that is used to be able to link to
        it (default empty, meaning it will be generated from the title)

        `no_toc`: Set this to `True` if the heading should not be
        included in the table of contents (default `False`)

        `returns`: The formatted heading

        """

        # Level is relative
        hlevel = self._get_real_hlevel(hlevel)

        # Create and return the header
        return self._mk_h(title, hlevel, hid, no_toc)
            
     
    def _md_doc(
            self,
            obj: object | str | list | None = None,
            name: str = "",
            title: str = "",
            hid: str = "",
            hlevel: int = 0,
            init: bool = False,
            complete: bool | list = False,
            init_title: str = "Initialize",
            skip_firstline: bool = False,
            name_transform: Callable = lambda n: n,
            title_transform: Callable = lambda n: n) -> str:
        R"""Insert the documentation of the given object

        Returns the documentation for the given object (class, method,
        function). If no object is given, the documentation of the
        module is returned.

        Arguments/return value:

        `obj`: The object (function, method, class) to prepare and
        return the documentation for. If `obj` is a list, the
        documentation for all objects in the list are prepared and
        returned (in separate paragraphs). If no object is given, the
        documentation for the module is prepared and returned
        (optional).
        
        `name`: The name of the object (optinal; we can find it)

        `title`: A title for the documentation if the heading is
        generated (optional; we will generate a proper title if
        `hlevel` is higher than zero and no title is given)

        `hid`: An id for the title that is used to be able to link to
        it (optional; will be genrated if needed and not given)

        `hlevel`: The heading level, cf. HTML h tag level (default 0,
        meaning no heading generated)

        `init`: Include the documentation and signature of the
        `__init__` method in the documentation of the object if the
        object is a class and has an `__init__` method (default
        `False`)

        `complete`: If the objetc is a class, include the
        documentation for the class, its constructor (the `__init__`
        method) and all non-hidden methods, when complete is `True`,
        or the listed methods, when complete is a list of methods
        (default `False`)

        `init_title`: If `complete` is set (`True` or a list) and the
        objetc is a class, use this combined with the class name as
        the title for the constructor (the `__init__` method)

        `skip_firstline`: The first line of the documentation string
        might have a specific meaning, like a title or a sub-title,
        and sometimes we might want to skip this part in the generated
        documentation.

        `name_transform`: a function that takes a text string as an
        argument and returns a text string; the function can be used
        to transform the (found) name

        `title_transform`:  a function that takes a text string as an
        argument and returns a text string; the function can be used
        to transform the (found) title

        `returns`: The documentation of the given object (or the module)

        """

        # The documentation of the module attribute
        adoc = ""

        # The special case, if `obj` is a list
        if type(obj) is list:

            # For each object, get the documentation
            for an_obj in obj:
                adoc += f"\n{self._md_doc(an_obj, hlevel=hlevel).strip()}\n"

            # Return the combined documentation
            return adoc
        
        # Level is relative
        org_hlevel = hlevel
        hlevel = self._get_real_hlevel(hlevel)

        # Get the object (attribute)
        if obj:
            if type(obj) is str:
                attr = _get_nested_attr(self.module, obj)
            else:
                attr = obj
            if not name:
                name = name_transform(attr.__qualname__)
        else:
            attr = self.module
            if not name:
                name = name_transform(self.name)
        
        # Get documentation string
        doc = _getdoc(attr).strip()

        # First line often have a special meaning (title or sub-title)
        firstline, doc = _special_first_line(doc)

        # If `hlevel` < 1 and a title, we don't need `hid` (and levelmarkers)
        
        # If `hlevel` >= 1, a title (and maybe `hid`) has to be is added
        if hlevel > 0 and not title:

            # Create `title` (and `hid`) from attribute
            for (ttype, ttest) in [
                    ("Class", isclass),
                    ("Method", _ismethod),
                    ("Function", isfunction),
                    ("Module", ismodule)]:
                if ttest(attr):
                    title = f"{ttype} `{name}`"
                    if hid:
                        hid = _mkid(hid, self.idlist)
                    else:
                        hid = _mkid(f"{name.lower()}", self.idlist)
                    break

            # Not able to create `title`, use first line as `title`
            else:

                # Get first line from `doc` and make it `title` + make `hid`
                if firstline:
                    title = firstline
                    firstline = None
                    if hid:
                        hid = _mkid(hid, self.idlist)
                    else:
                        hid = _mkid(title, self.idlist)
                else:
                    raise PyPiMDocError("Unable to find title for doc string")

        # Get signature if method 
        if isfunction(attr):
            sig = _signature(attr)

        # Signture of class from `__init__` (and its documentation string)
        elif isclass(attr) and hasattr(attr, "__init__") and init:
            init_doc = _getdoc(attr.__init__)
            fline, init_doc = _special_first_line(_getdoc(attr.__init__))
            if fline:
                init_doc = f"**{fline}**\n\n{init_doc}"
            if init_doc:
                doc += f"\n\n{init_doc}"
            sig = _signature(attr.__init__)
            
        # No signature
        else:
            sig = None

        # Add the title to the module doc
        if title:
            adoc += self._mk_h(title_transform(title), hlevel, hid)

        # Add signature
        if sig:
            if "." in name:
                fname = name.split(".")[-1]
            else:
                fname = name
            adoc += f"\n```python\n{fname}{sig}\n```\n"

        # Arguments/Returns headers in the documentation string
        doc = _margsheader.sub(r'\n\n{{\1}}\n\n', doc, re.MULTILINE)
        doc = doc.replace("{{", "**").replace("}}", "**")
        
        # Complete class, including methods
        if complete and isclass(attr):

            # Include the constructor (`__init__`) if implemented
            if (not init and hasattr(attr, "__init__")
                and _ismethod(attr.__init__)):
                method_kw_list = [
                    {"obj": attr.__init__,
                     "name": name,
                     "title": f"{init_title} `{name}`"}]
            else:
                method_kw_list = []

            # The methods are listed
            if type(complete) is list:
                method_kw_list += [{"obj": m} for m in complete]

            # If complete is not a list, find all public methods
            else:
                for n in dir(attr):
                    m = getattr(attr, n)
                    if _ismethod(m) and m.__name__[0] != "_":
                        method_kw_list.append({"obj": m})

            # Add the documentation for the methods of the class
            for kw in method_kw_list:
                kw["hlevel"] = org_hlevel + 1 if org_hlevel > 0 else 0
                kw["name_transform"] = name_transform
                doc += "\n\n" + self._md_doc(**kw)

        # Add the documentation string to the module doc
        if firstline and not skip_firstline:
            doc = f"*{firstline}*\n\n{doc}"
        adoc += f"\n{doc}\n"

        # Return the documentation of the object (or module)
        return adoc
    

    def _md_bdoc(
            self,
            hlevel: int = 0,
            init: bool = False,
            complete: bool | list = False,
            init_title: str = "Initialize",
            skip_firstline: bool = False,
            name_transform: Callable = lambda n: n,
            title_transform: Callable = lambda n: n):
        R"""The following lines list objects to document

        The non-empty lines between the MD-methods `bdoc` (implemented
        here) and `edoc` are interpreted as list of objects
        (functions, classes, methods) where the documentation should
        be inserted here. The arguments are similar to the arguments to
        the MD-method `doc` with the exception of the object specific
        arguments that have no valid meaning for a list of objects
        (`obj`, `name`, `title`, `hid`).

        Arguments:

        `hlevel`: The heading level, cf. HTML h tag level (default 0,
        meaning no heading generated)

        `init`: Include the documentation and signature of the
        `__init__` method in the documentation of the object if the
        object is a class and has an `__init__` method (default
        `False`)

        `complete`: If the objetc is a class, include the
        documentation for the class, its constructor (the `__init__`
        method) and all non-hidden methods, when complete is `True`,
        or the listed methods, when complete is a list of methods
        (default `False`)

        `init_title`: If `complete` is set (`True` or a list) and the
        objetc is a class, use this combined with the class name as
        the title

        `skip_firstline`: The first line of the documentation string
        might have a specific meaning, like a title or a sub-title,
        and sometimes we might want to skip this part in the generated
        documentation.

        `name_transform`: a function that takes a text string as an
        argument and returns a text string; the function can be used
        to transform the (found) name

        `title_transform`:  a function that takes a text string as an
        argument and returns a text string; the function can be used
        to transform the (found) title

        """
        self.bdoc = self.mlns["args_kw"](
            hlevel = hlevel, init = init, complete = complete,
            init_title = init_title, skip_firstline = skip_firstline,
            name_transform = name_transform, title_transform = title_transform)

        
    def _md_edoc(self) -> str:
        R"""Terminate the list of objects to document

        This MD-method terminate the list of objects to genereate the
        documentation for, and returns the complete documentation of
        all the objects.

        Return value:

        `returns`: The documentation of all the objects

        """
        doc = ""
        args, kw = self.bdoc
        for obj in self.objlist:
            doc += "\n\n" + self._md_doc(obj, *args, **kw) + "\n\n"
        self.bdoc = ()
        self.objlist = []
        return doc

    
    def _md_toc(self, name: str = "toc", btoc: bool = True,
            toc_item_start: str = " - ", toc_item_end: str = "\n",
            toc_item_indent: int = 4) -> str:
        R"""Insert a table of contents

        Insert a table of contents with all headings following this
        MD-method until the end of document or until a matching `etoc`
        MD-method. If the `btoc` argument is `False`, the table of
        contents will be inserted here but items (headings) for the
        table of contents will not be registered yet. You then need to
        insert a `btoc` MD-method in the README template to start
        collcting items for the table of contents.

        Is is also possible to have different sets of table of
        contents.  To do this, give each set a unique name (the
        default name is `"toc"`).
        
        Arguments/return value:

        `name`: The name of this specific table of contents; only
        needed if you have different sets og groups of table of
        contents in the README template (optional, default `"toc"`)

        `btoc`: If `False`, do not start to collect items for the
        table of contents here (default `True`)

        `toc_item_start`: The text string preceeding every item in the
        table of contents (default `" - "`)

        `toc_item_end`: The text string following every item in the
        table of contents (default `"\n"`)

        `toc_item_indent`: (default 4)

        `returns`: The formatted version of the table of contents

        """

        # Start collecting items to table of contents (with the given name)
        if btoc:
            self._md_btoc(name)

        # The datastructure for this table of contents
        self.tocpart[name] = {
            "items" : [],
            "toc_item_start": toc_item_start,
            "toc_item_end": toc_item_end,
            "toc_item_indent": toc_item_indent
            }

        # Return a placeholder for the table of contents
        return f"%({name})s"

    
    def _md_btoc(self, name: str = "toc"):
        R"""Start to collect items to table of contents

        Start to collect items to table of contents (with the given
        name).  From now on and until the matching `etco` MD-method or
        the end of the file, every heading will be added as an item to
        the table of contents (with the exceptions of headings marked
        not to be added to table of contents).

        Arguments:

        `name`: The name of this specific table of contents; only
        needed if you have different sets og groups of table of
        contents in the README template (optional, default `"toc"`)

        """
        self.mktoc.add(name)
        
        
    def _md_etoc(self, name: str = "toc"):
        R"""Stop collecting items to table of contents

        Stop collecting items to table of contents (with the given
        name).
        
        Arguments:
        
        `name`: The name of this specific table of contents; only
        needed if you have different sets og groups of table of
        contents in the README template (optional, default `"toc"`)
        
        """
        self.mktoc.discard(name)

        
    def _md_eval(self, code: str) -> str:
        R"""Insert the text output of the Python code

        Insert the text output of the Python code evaluated in the
        name space of the module and the MD-methods’ local name space.
        
        Arguments/return value:

        `code`: The Python code to evaluate

        `returns`: The resulting text

        """
        return eval(code, globals=self.mgns)

    
    def _md_code(self, code: str):
        R"""Execute the code 

        Execute the code to populate the MD-methods’ local name space
        that later can be used in MD-methods arguments and in the code
        of the MD-method `eval`.

        Arguments:

        """
        exec(code, globals=self.mgns, locals=self.mlns)

        
    def _md_bcode(self):
        R"""The start of a code block to execute

        Execute the code between this MD-method and the next `ecode`
        MD-method. The code is used to populate the MD-methods’ local
        name space that later can be used in MD-methods arguments and
        in the code of the MD-method `eval`.

        """
        self.code = "# Code from templates follows below\n"

        
    def _md_ecode(self):
        R"""The end of a code block to execute

        Execute the code between the previous `bcode` MD-method and
        this MD-method. The code is used to populate the MD-methods’
        local name space that later can be used in MD-methods
        arguments and in the code of the MD-method `eval`.

        """
        self._md_code(self.code)
        self.code = ""

        
    def _md_cmd(self, cmd: str) -> str:
        R"""Insert the text output of the command

        Insert the text output of the (shell) command.

        Arguments/return value:

        `cmd`: The shell command

        `returns`: The output of the command
        
        """
        cmdl = cmd.split()
        res = subprocess.run(cmdl, text=True, capture_output=True)
        if res.returncode != 0:
            raise PyPiMDocError(f"Command failed{cmd}")
        else:
            return res.stdout.strip()
        

    def _md_cmd_cb(self, cmd: str) -> str:
        R"""Insert the text output of the command as a code block

        Insert the text output of the (shell) command as a code block.

        Arguments/return value:
        
        `cmd`: The shell command

        `returns`: The output of the command in a code block
        
        """
        return f"```\n{self._md_cmd(cmd)}\n```\n"
    

    def _md_help(self, title: str = "", cmd: str = "", hlevel: int = 0,
                 hid: str = '', no_toc: bool = False) -> str:
        R"""Insert the output from a help command

        Insert the output from a help command reformatted as markdown.
        The output of the help command is expected to be formated as
        the Python module `argparse` formats the help text.
        
        Arguments/return value:

        `title`: The title used in the heading (create a default title
        if this is not provided)

        `cmd`: The help command (default empty, meaning execute the
        current moudule's file module with the command line argument
        `"-h"`)

        `hlevel`: The heading level for the title (default 0, meaning
        no heading)

        `hid`: An id for the title that is used to be able to link to
        it (default empty, meaning it will be generated from the
        title)

        `no_toc`: Set this to `True` if the heading should not be
        included in the table of contents (default `False`)

        `returns`: The heading and output of the help command formated

        """

        # Make the heading (with title), if needed
        if hlevel > 0:
            if not title:
                title = f"Command `{self.name}`"
            heading = self._md_h(title, hlevel, hid, no_toc) + "\n\n"
        else: 
            heading = ""

        # Get the help text
        if not cmd:
            cmd = f"{sys.executable} {self.filename} -h"

        # Get help text and convert it to markdown
        help_txt = self._md_cmd(cmd)
        md_txt = help2md(help_txt)
        
        # Return heading and help text
        return heading + md_txt


# More help functions

def _list_md_methods(
        cls: object = PyPiMDoc,
        pre: str = "_md_",
        rm_pre: bool = False,
        qualname: bool = True,
        sort_order: list | None = [
            "^h$", "([be])?doc", "([be])?toc", "eval", "([lbe])?code",
            "[l]?cmd", "help"
        ]) -> list:
    R"""List all the MD-methods

    List all the MD-methods if the given object or class.

    Arguments/return value:

    `cls`: Class or object to list the MD-methods from (default `PyPiMDoc`)

    `pre`: The pre-string of all MD-methods (default `"_md_"`)

    `rm_pre`: Remove the pre-string from the name of ech method in the
    list (default `False`)

    `qualname`: Use the fully qualified name of the methods (include
    the class name, default `True`)

    `sort_order`: A list of regular expressions specifing the sort
    order in the returned list of method names; if this is `None` no
    extra sorting is done (for the regular expression with a group,
    names with an empty group are put in front of the other ones
    matching the same regular expressions; see the default value in
    the method definition)

    `returns`: The list of MD-method names

    """

    # Find the MD methods (with the names starting with `pre`)
    psize = len(pre)
    mdm = [m for m in dir(cls) if m[:psize] == pre]

    # Use the fully qualified name?
    if qualname:
        mdm = [getattr(cls, m).__qualname__ for m in mdm]

    # Or remove the first part of the name, the `pre` string
    elif rm_pre:
        mdm = [m[psize:] for m in mdm]

    # Should the method names be sorted in a specific order?
    if sort_order:

        # Do the sorting by groups (the sort order groups)
        mdm_sort = {so: [] for so in sort_order}
        rest = []
        for m in mdm:
            for so in sort_order:
                ma = m.split(".")[-1]
                if ma[:psize] == pre:
                    ma = ma[psize:]
                if me:=re.match(so, ma):
                    if me.groups() and not me.group(1):
                        mdm_sort[so] = [m] + mdm_sort[so]
                    else:
                        mdm_sort[so].append(m)
                    break
            else:
                rest.append(m)

        # Morge the groups to a single sorted list
        mdm = []
        for so in sort_order:
            mdm += mdm_sort[so]
        mdm += rest

    # Return a list of the (sorted) method names
    return mdm


#
# The rest of the code is to run the module as an interactive command
#
        
# Execute this module as a program
def main():

    # Formatters
    formatters = ["markdown", "html", "latex"]

    # Create overall argument parser
    import argparse
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0])
    parser.add_argument(
        "pysrc", metavar="PYSRC",
        help="module source code file")
    parser.add_argument(
        "-V", "--version", action="version",
        version=f"%(prog)s " + version)
    parser.add_argument(
        "-t", "--template",
        type=argparse.FileType("r"),
        help="markdown template (default 'README.template')")
    parser.add_argument(
        "-o", "--outfile", default=sys.stdout, type=argparse.FileType("w"),
        help="output file (default stdout)")
    parser.add_argument(
        "-f", "--formatter", default=None, choices=formatters,
        help="formatter to use (default guessed by filename or 'markdown')")
    parser.add_argument(
        "-s", "--style", default="emacs",
        help="style (default 'emacs')")
    parser.add_argument(
        "-l", "--base-heading-level", default=1, type=int,
        help="base (start) level of headings " + \
          "(default 1, like '<h1></h1>' in HTML)")
    parser.add_argument(
        "-n", "--name", default=None,
        help="name of module (default source code filename without '.py')")
    
    # Parse arguments
    args = parser.parse_args()

    # Choose formatter (html or latex)
    if args.formatter:
        if args.formatter == "html":
            formatter = HtmlFormatter()
        elif args.formatter == "latex":
            formatter = LatexFormatter()
        else:
            formatter = None
    else:
        if Path(args.outfile.name).suffix in [".html", ".htm"]: 
            formatter = HtmlFormatter()
        elif Path(args.outfile.name).suffix in [".ltx", ".tex", ".latex"]: 
            formatter = LatexFormatter()
        else:
            formatter = None
            
    # Choose style
    try:
        style = get_style_by_name(args.style)
    except ClassNotFound:
        print(f"{sys.argv[0]}: unknown style {args.style}", file=sys.stderr)
        sys.exit(1)

    # Create `PyPiMDoc` instance and create the documentation
    pypimdoc = PyPiMDoc(args.pysrc, base_heading_level=args.base_heading_level)
    md = pypimdoc.process_template(args.template)
    print(md, file=args.outfile)


# execute this module as a program
if __name__ == '__main__':
    main()
