

### <a id="module-pypimdoc"></a>A Python module for generating Python module documentation

When developing Python modules, documentation is important. The source
code of a Python module inludes a lot of documentation, including
documentation strings, comments and code. The goal of the `pymdoc`
module is to use the documentation found in the source code and
produced by the module itself, instead of writing separate documents
describing the features of the module. Based on a template file, the
documentation is generated from the source code of the module. As a
consequence, when the source code of the module (including the
documentation strings) is updated, the documentation of the module is
also updated.

The module and its console script were developed to generate the
documentation at [PyPi](https://pypi.org/) of my own Python modules,
including [this module](https://pypi.org/project/pymdoc/), the
[`webinteract`](https://pypi.org/project/webinteract/) module and the
[`onepw`](https://pypi.org/project/onepw/) module.

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


**Table of contents**

 - <a href="#pypimdoc1">Class `PyPiMDoc`</a>
     - <a href="#Initialize+%60PyPiMDoc">Initialize `PyPiMDoc`</a>
     - <a href="#pypimdoc.process_me1">Method `PyPiMDoc.process_method`</a>
     - <a href="#pypimdoc.process_te1">Method `PyPiMDoc.process_template`</a>
 - <a href="#help2md1">Function `help2md`</a>
 - <a href="#Module+documentation">Module documentation methods</a>
     - <a href="#h1">MD-method `h`</a>
     - <a href="#doc1">MD-method `doc`</a>
     - <a href="#bdoc1">MD-method `bdoc`</a>
     - <a href="#edoc1">MD-method `edoc`</a>
     - <a href="#toc1">MD-method `toc`</a>
     - <a href="#btoc1">MD-method `btoc`</a>
     - <a href="#etoc1">MD-method `etoc`</a>
     - <a href="#eval1">MD-method `eval`</a>
     - <a href="#code1">MD-method `code`</a>
     - <a href="#bcode1">MD-method `bcode`</a>
     - <a href="#ecode1">MD-method `ecode`</a>
     - <a href="#cmd1">MD-method `cmd`</a>
     - <a href="#cmd_cb1">MD-method `cmd_cb`</a>
     - <a href="#help1">MD-method `help`</a>
 - <a href="#To+use+the+module+as">To use the module as a console script</a>
     - <a href="#Command+%60pypimdoc%60">Command `pypimdoc`</a>

### <a id="pypimdoc1"></a>Class `PyPiMDoc`

*The Python module documentation class*

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


#### <a id="Initialize+%60PyPiMDoc"></a>Initialize `PyPiMDoc`

```python
PyPiMDoc(filename: str, name: str = '', base_heading_level: int = 1, toc_begin: int = 1, toc_end: int = 3)
```

*Initialize a Python module documentation object*

Initialize a Python module documentation object, including
loading the Python module (Python source code) and prepare the
document generation.

**Arguments:**

`filename`: The file name of the module to document

`name`: The name of the module (default generated from the
`filename`)

`base_heading_level`: All generated headings are at this level
or above (default 1)

`toc_begin`: Include items in table of contents from this
level (relative to `base_heading_level`, default 1)

`toc_end`: Include items in table of contents to this level
(relative to `base_heading_level`, default 2)



#### <a id="pypimdoc.process_me1"></a>Method `PyPiMDoc.process_method`

```python
process_method(method_name: str, args_str: str) -> str
```

*Process a MD-method*

Process a MD-method with the given name and arguments.

**Arguments/return value:**

`method_name`: MD-method name

`args_str`: the arguments to the MD-method as a string

`returns`: returns the documentation part generated by the MD-method



#### <a id="pypimdoc.process_te1"></a>Method `PyPiMDoc.process_template`

```python
process_template(template: io.TextIOBase) -> str
```

*Read and process template*

The template file is the driver of the document generation. In
its simplest form, the template is a markdown document that
becomes the module documentation. The template includes some
special commands (MD-methods) used to fetch documentation from
the module (including the documentation strings in the
module).

**Arguments/return value:**

`template`: The README template file

`returns`: The processed markdown README file content



### <a id="help2md1"></a>Function `help2md`

```python
help2md(help_msg: str) -> str
```

*Convert a help message to markdown*

Convert a help message (the output from a command when the `-h`
flag is given) to a valid and well-formated markdown text.

The function is inspired by the awk script
[`help2md`](https://github.com/valeriangalliat/help2md) and my own
version of this awk script updated to better match the help
message generated by the `argparse` module:
`help2md-argparse.awk`.

**Arguments/return value:**

`help_msg`: The help message to convert

`returns`: The markdown text


### <a id="Module+documentation"></a>Module documentation methods

The module documentation methods (MD methods) are used in the README
template to get documentation and iformation from the Python module
documented. For example, the following line creates the complete
documentation of the class `PyPiMDoc` (including all public methods):
```
<!-- doc(PyPiMDoc, hlevel = 1, complete = True) -->
```
The previous section, <a href="#pypimdoc1">Class `PyPiMDoc`</a>, is an
example of the result of such an MD method.




#### <a id="h1"></a>MD-method `h`

```python
h(title: str, hlevel: int, hid: str = '', no_toc: bool = False) -> str
```

*Insert a heading*

Insert a heading at the given level (including adjustment
from base level).

**Arguments/return value:**

`title`: A title

`hlevel`: The heading level for the title

`hid`: An id for the title that is used to be able to link to
it (default empty, meaning it will be generated from the title)

`no_toc`: Set this to `True` if the heading should not be
included in the table of contents (default `False`)

`returns`: The formatted heading





#### <a id="doc1"></a>MD-method `doc`

```python
doc(obj: object | str | list | None = None, name: str = '', title: str = '', hid: str = '', hlevel: int = 0, init: bool = False, complete: bool | list = False, init_title: str = 'Initialize', skip_firstline: bool = False, name_transform: collections.abc.Callable = <function PyPiMDoc.<lambda> at 0x10384bce0>, title_transform: collections.abc.Callable = <function PyPiMDoc.<lambda> at 0x10384bd80>) -> str
```

*Insert the documentation of the given object*

Returns the documentation for the given object (class, method,
function). If no object is given, the documentation of the
module is returned.

**Arguments/return value:**

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





#### <a id="bdoc1"></a>MD-method `bdoc`

```python
bdoc(hlevel: int = 0, init: bool = False, complete: bool | list = False, init_title: str = 'Initialize', skip_firstline: bool = False, name_transform: collections.abc.Callable = <function PyPiMDoc.<lambda> at 0x10384bec0>, title_transform: collections.abc.Callable = <function PyPiMDoc.<lambda> at 0x10384bf60>)
```

*The following lines list objects to document*

The non-empty lines between the MD-methods `bdoc` (implemented
here) and `edoc` are interpreted as list of objects
(functions, classes, methods) where the documentation should
be inserted here. The arguments are similar to the arguments to
the MD-method `doc` with the exception of the object specific
arguments that have no valid meaning for a list of objects
(`obj`, `name`, `title`, `hid`).

**Arguments:**

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





#### <a id="edoc1"></a>MD-method `edoc`

```python
edoc() -> str
```

*Terminate the list of objects to document*

This MD-method terminate the list of objects to genereate the
documentation for, and returns the complete documentation of
all the objects.

**Return value:**

`returns`: The documentation of all the objects





#### <a id="toc1"></a>MD-method `toc`

```python
toc(name: str = 'toc', btoc: bool = True, toc_item_start: str = ' - ', toc_item_end: str = '\n', toc_item_indent: int = 4) -> str
```

*Insert a table of contents*

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

**Arguments/return value:**

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





#### <a id="btoc1"></a>MD-method `btoc`

```python
btoc(name: str = 'toc')
```

*Start to collect items to table of contents*

Start to collect items to table of contents (with the given
name).  From now on and until the matching `etco` MD-method or
the end of the file, every heading will be added as an item to
the table of contents (with the exceptions of headings marked
not to be added to table of contents).

**Arguments:**

`name`: The name of this specific table of contents; only
needed if you have different sets og groups of table of
contents in the README template (optional, default `"toc"`)





#### <a id="etoc1"></a>MD-method `etoc`

```python
etoc(name: str = 'toc')
```

*Stop collecting items to table of contents*

Stop collecting items to table of contents (with the given
name).

**Arguments:**

`name`: The name of this specific table of contents; only
needed if you have different sets og groups of table of
contents in the README template (optional, default `"toc"`)





#### <a id="eval1"></a>MD-method `eval`

```python
eval(code: str) -> str
```

*Insert the text output of the Python code*

Insert the text output of the Python code evaluated in the
name space of the module and the MD-methods’ local name space.

**Arguments/return value:**

`code`: The Python code to evaluate

`returns`: The resulting text





#### <a id="code1"></a>MD-method `code`

```python
code(code: str)
```

*Execute the code*

Execute the code to populate the MD-methods’ local name space
that later can be used in MD-methods arguments and in the code
of the MD-method `eval`.

Arguments:





#### <a id="bcode1"></a>MD-method `bcode`

```python
bcode()
```

*The start of a code block to execute*

Execute the code between this MD-method and the next `ecode`
MD-method. The code is used to populate the MD-methods’ local
name space that later can be used in MD-methods arguments and
in the code of the MD-method `eval`.





#### <a id="ecode1"></a>MD-method `ecode`

```python
ecode()
```

*The end of a code block to execute*

Execute the code between the previous `bcode` MD-method and
this MD-method. The code is used to populate the MD-methods’
local name space that later can be used in MD-methods
arguments and in the code of the MD-method `eval`.





#### <a id="cmd1"></a>MD-method `cmd`

```python
cmd(cmd: str) -> str
```

*Insert the text output of the command*

Insert the text output of the (shell) command.

**Arguments/return value:**

`cmd`: The shell command

`returns`: The output of the command





#### <a id="cmd_cb1"></a>MD-method `cmd_cb`

```python
cmd_cb(cmd: str) -> str
```

*Insert the text output of the command as a code block*

Insert the text output of the (shell) command as a code block.

**Arguments/return value:**

`cmd`: The shell command

`returns`: The output of the command in a code block





#### <a id="help1"></a>MD-method `help`

```python
help(title: str = '', cmd: str = '', hlevel: int = 0, hid: str = '', no_toc: bool = False) -> str
```

*Insert the output from a help command*

Insert the output from a help command reformatted as markdown.
The output of the help command is expected to be formated as
the Python module `argparse` formats the help text.

**Arguments/return value:**

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




### <a id="To+use+the+module+as"></a>To use the module as a console script


#### <a id="Command+%60pypimdoc%60"></a>Command `pypimdoc`


*A Python module for generating Python module documentation*

**Usage:**

```bash
pypimdoc [-h] [-V] [-t TEMPLATE] [-o OUTFILE] [-f {markdown,html,latex}] [-s STYLE] [-l BASE_HEADING_LEVEL] [-n NAME] PYSRC
```

**Positional arguments:**

Name | Description
---- | -----------
`PYSRC` | module source code file

**Options:**

Name | Description
---- | -----------
`-h, --help` | show this help message and exit
`-V, --version` | show program's version number and exit
`-t, --template TEMPLATE` | markdown template (default `README.template`)
`-o, --outfile OUTFILE` | output file (default stdout)
`-f, --formatter {markdown,html,latex}` | formatter to use (default guessed by filename or `markdown`)
`-s, --style STYLE` | style (default `emacs`)
`-l, --base-heading-level BASE_HEADING_LEVEL` | base (start) level of headings (default 1, like `<h1></h1>` in HTML)
`-n, --name NAME` | name of module (default source code filename without `.py`)



