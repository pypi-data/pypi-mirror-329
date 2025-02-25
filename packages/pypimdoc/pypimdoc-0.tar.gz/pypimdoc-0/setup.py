import os

from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
requires = []

from setuptools.command.egg_info import egg_info
class egg_info_ex(egg_info):
    """Includes license file into `.egg-info` folder."""
    def run(self):
        # don't duplicate license into `.egg-info` when building a distribution
        if not self.distribution.have_run.get('install', True):
            # `install` command is in progress, copy license
            self.mkpath(self.egg_info)
            self.copy_file('LICENSE', self.egg_info)
        egg_info.run(self)
        
setup(
    name='pypimdoc',
    version='0',    
    description='A Python module for generating Python module documentation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://www.pg12.org/software',
    project_urls={
        "Download": "https://www.pg12.org/dist/py/lib/pypimdoc/",
    },
    author='A Andersen',
    author_email='a.andersen@pg12.org',
    license='Modified BSD License',
    license_files = ('LICENSE',),
    cmdclass = {'egg_info': egg_info_ex},
    packages=['pypimdoc'],
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'pypimdoc=pypimdoc:main']},
    classifiers=[
        'License :: OSI Approved :: BSD License',  
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
