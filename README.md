# README #
pymake2 is a simple Python-based make system. It brings simplicity and flexibility of Python language to makefiles. The name 'pymake2' is chosen because 'pymake' is already used for another tool that re-implements the GNU make in python. pymake2 is different from pymake as it does not try to re-implements GNU make, but a new simple make system that uses Python for makefiles to leverage the language richness and flexibility. pymake2 parses makefile-like python scripts and provides useful messages to help understand what goes wrong during the build process.


### How to install pymake2 ###

1. You can use `pip` to automatically download and install `pymake2` from the PyPi repository using the following command:

    for the current user (user-site-packages):

    ```
    pip install --user pymake2
    ```

    for system-wide installation:

    ```
    sudo pip install pymake2
    ``` 

2. You can always clone the repository and install it manually by running the following command:

    ```
    python setup.py install
    ```


### Using pymake2 ###
```
#> pymake2 -h
usage: pymake2 [-h] [-f MakefilePath] [-j Jobs] Target

pymake2 is a simple make system implemented in python

positional arguments:
  Target           the make target in the makefile

optional arguments:
  -h, --help       show this help message and exit
  -f MakefilePath  to pass a makefile, default = ./makefile.py
  -j Jobs          number of jobs used in the make process
#> 

```
pymake2 looks into the current working directory for the default `makefile.py` and provides tab-auto-complete for the targets in that makefile. If the option `-f /path/to/makefile.py` is used, pymake2 provides tab-auto-complete for the targets in selected makefile instead.

The following snippet shows a makefile example for arbitrary gcc-based C99 project. 

```python
from pymake2 import *
Debug = True # <-- set it to True to enable more debugging messages 
# HighlightErrors = True # To enable the highliter
HighlightWarnings = True # To enable the highliter
HighlightNotes = True # To enable the highliter

# Custom Highlighting using regular expressions
hl(regx(r'error:.+'), colors.IRed)
# hl(regx(r'expression'), colors.IGreen, colors.On_Cyan)
# hl('c', colors.IGreen)


CC = 'gcc'
CFLAGS = '-g -O2 -std=c99'
LINKFLAGS = ''

executable = 'a.out'
BUILDdir = './Build/'
src_files = find(root='./', filter='*.c')
obj_files = replace(src_files, '.c', '.o')
obj_files = retarget(obj_files, BUILDdir, '')


@target
def all(Tlink): # depends on Target link
  printcolor('Build Succeeded', colors.IGreen)
  return True

@target
def Tlink(Tcompile): # depends on Target compile
  return link(CC, LINKFLAGS, obj_files, executable)

@target
def Tcompile(src_files): # depends on srource files
  return compile(CC, CFLAGS, src_files, obj_files)
    


@target
def clean():
  retV = run(eval('rm -r $(BUILDdir)'))
  retV = run(eval('rm $(executable)'))
  return True

```
First of all, `makefile.py` must import pymake2. To enable detailed error messages in the build process, `Debug` variable should be set to True. The above snippet is self-explanatory to any one used to work with makefiles. 

The following makefile example is for arbitrary latex project:
```python
from pymake2 import *
Debug = True # <-- set it to True to enable more debugging messages 
HighlightErrors = True # To enable the highliter
HighlightWarnings = True # To enable the highliter
HighlightNotes = True # To enable the highliter

latexfile = 'main.tex'
pdffile = 'main.pdf'

@target
def all(pdf):
    printcolor('Build Succeded', colors.Green)
    return True

@target
def pdf(latexfile):
    if run(eval('pdflatex -shell-escape -halt-on-error $(latexfile)'), True, True):
        printcolor('Build Succeded', fg='32', B=True)
        run(eval('evince $(pdffile)&'))
        return True

@target
def clean():
    retV = run(eval('rm -f *.aux *.log *.blg *.bbl *.synctex.gz *.out *.cut $(pdffile) *.vtc'), True)
    return retV

```


### Features of pymake2 ###
- `makefile.py` follows similar approach of GNU make, but with the flexibility of Python
- pymake2 automatically highlights error, warning, and info messages produced by the compiler or the linker. This is especially useful when the used toolchain does not prints colorful outputs. As shown in the snippet above, to get highlighted outputs, you need to enable `HighlightErrors`, `HighlightWarnings`, and `HighlightNotes`, or use custom highlighting as needed. The highlighted outputs only works with the commands provided by pymake2 such as `compile`, `link`, and `archive` and not with `shell`, `sh`, or `run` commands.
- the `eval` function recognizes the format of makefile-like variables, such as `$(BUILDdir)` and `$(CC)`, ...etc. This feature helps to port existing makefiles to pymake2. In addition, the `eval` function evaluates environment variables in the same way. However, variables defined in the makefile has precedence over the environment variables. In other words, redefining environment variables in the makefile overrides them.
- the target function accepts unlimited number of arguments to specify dependencies.
    - the dependency can be another target function/s, or a list of files.
    - pymake2 tries to satisfy all the dependences before invoking the target function.
    - if a target function is in the dependency list of another target function, it must return True upon success.
- pymake2 provides a set of helper functions; below I list some of them, see `make.py` in the source files for more details about their parameters.
    - `shell('cmd')` and `sh('cmd')`: runs the shell command and return the output.
    - `run('cmd')`: runs the shell command without returning the output.
    - `compile(...)`: if necessary, compiles the source files using the specified compiler along with the passed flags.
    - `link(...)`: if necessary, links the object files to provide the executable using the passed linker and flags.
    - `archive(...)`: if necessary, archives the object files to provide the output library using the passed archiver such as `gcc-ar` along with the passed flags.
- pymake2 automatically recognizes space-separated lists (used in makefiles for source or object files) and converts them to Python lists. Therefore, the commands provided by pymake2 such as `compile` and `link` accepts both formats (Python list, and space-separated list).

###Screenshots###
Succesfull build with highlighted compile warnings.

![alt text](https://bytebucket.org/saudalwasly/pymake2/raw/eb224dac994da5fb0d660edf19ac2792e46544e9/screenshots/screenshot_1.png "screenshot example of a successful build")


Rebuilding the same target yields already satisfied dependencies and not need to recompile and link.

![alt text](https://bytebucket.org/saudalwasly/pymake2/raw/eb224dac994da5fb0d660edf19ac2792e46544e9/screenshots/screenshot_2.png "screenshot example of a successful build")



Building for the target `Tlib` failed after cleaning as it depends on all object files `OBJ_All`.

![alt text](https://bytebucket.org/saudalwasly/pymake2/raw/eb224dac994da5fb0d660edf19ac2792e46544e9/screenshots/screenshot_3.png "screenshot example of a failed on dependency")


### License ###
pymake2 is distributed under MIT license.

Copyright (c) 2016 Saud Wasly

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.