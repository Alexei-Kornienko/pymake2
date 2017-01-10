# README #
pymake2 is a simple Python-based make system. It brings simplicity and flexibility of Python language to makefiles. The name 'pymake2' is chosen because 'pymake' is already used for another tool that re-implements the GNU make in python. pymake2 is different from pymake as it does not try to re-implements GNU make, but a new simple make system that uses Python for makefiles to leverage the language richness and flexibility. pymake2 parses makefile-like python scripts and provides useful messages to help understand what goes wrong during the build process.


### How to install pymake2 ###
1. you can always clone the repository and install it manually by copying the files to a destination directory and add it to the $PATH
2. for Debian-based systems such Ubuntu I suggest to use the .deb package provided in the download section ([click-here](https://bitbucket.org/saudalwasly/pymake2/downloads))
    * then you can install it by running the following command:
    ```
    sudo dpkg -i pymake2_X.X-X.deb    
    ```
    * to uninstall it, just use the following command:
    ```
    sudo apt-get remove pymake2
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

The following snippet shows a makefile example. 

```python
from pymake2 import *
Debug = False # <-- set it to True to enable more debugging messages 
HighlightErrors = True # To enable the highliter
HighlightWarnings = True # To enable the highliter
HighlightNotes = True # To enable the highliter
#######################################################
# Project Specifications
# Specificity the Executable output file
executable = 'out.elf'
BUILDdir = './build'
############ Specify the linker script
LikerScript = '-T lscript.ld'
#ERAPlatformDir= '/path/ERAPlatform/'
ERAPlatformDir = eval('$(ERAPlatformDir)') # it will get it from the environment variables if it is not defined in the file
ERAsimDrivers = eval('$(ERAPlatformDir)/ERAsimDrivers')

#ERAdrivers includes
ERAIncludes = shell(eval("sfind $(ERAsimDrivers) -r -d -a"))
ERAIncludes += eval(' $(ERAsimDrivers)')

# Project Includes
# include all the directories and sub directories the project folder.
ProjIncludes = join('./', shell('sfind ./ -r -d'))

Includes = eval('$(ProjIncludes) $(ERAIncludes)').split()
Includes = ['-I %s'%item for item in Includes]

# Startup assembly files files
CPU0Startup         = 'src/CPU0' # .s
CPU1Startup         = 'src/CPU1' # .s
startobj            = 'src/CPU0.o src/CPU1.o'

# include all the .c files in the project directory and sub directories.
CSRC_Project = shell('sfind ./ -r -f "*.c"')
CSRC_ERADrivers = shell(eval("sfind $(ERAsimDrivers) -r -f '*.c' -a"))
CSRC_ALL = eval('$(CSRC_Project) $(CSRC_ERADrivers)')

OBJ_Project = replace(CSRC_Project, '.c', '.o')
OBJ_ERADrivers = replace(CSRC_ERADrivers, '.c', '.o')

OBJ_All  = eval('$(OBJ_Project) $(OBJ_ERADrivers)').split()
OBJ_All  = replace(OBJ_All, ERAPlatformDir, '') # <-- remove the prefix for obj files
OBJ_All  = [BUILDdir + '/' + e for e in OBJ_All] # <-- To redirect the build directory
OBJ_All  = normpaths(OBJ_All) # a nice obj-files list directed in the build folder

#######################################################
## toolchain specification
CC                  = 'mips-gcc'
AR                  = 'mips-ar'
IncludePaths        = Includes
LibPaths            = '-L $(ERAPlatformDir)/mips/'
CFLAGS              = eval('-std=c99 -nostdlib -O1 -msoft-float -march=mips1 -EL -g -Wall $(IncludePaths)')
LINKFLAGS           = eval('$(LikerScript) -nostdlib -march=mips1 -ffreestanding -EL -Xlinker -Map=output.map $(LibPaths) -lc')
########################################################

################## Targets #############################
@target
def all(Tlink): # <-- depends on the target "Tlink"
  run('mips-objdump -D %s > disassembly.txt'%executable)
  run('mips-readelf -a %s > elfdump.txt'%executable)
  run('mips-objdump --dwarf=info %s > dwarfinfo.txt'%executable)
  run('mips-size %s'%executable)
  printcolor('build succeeded', fg='32', B=True)
  return True

@target
def Tlink(Tcompile): # <-- depends on the target "Tcompile"
  if link(CC, LINKFLAGS, join(startobj, OBJ_All), executable):
    return True

@target
def Tcompile(CSRC_ALL): # <-- depends on all source files
  if compile(CC, CFLAGS, CSRC_ALL, OBJ_All):
    return True

@target
def Tlib(OBJ_All): # <-- depends on all object files
  if archive(AR, 'ru', OBJ_All, 'lib.a'):
    return True

@target
def startup(['CPU0Startup.s', 'CPU0Startup.s']): # accepts str, list, and function
   shell(eval('$(CC) -c $(CFLAGS) $(CPU0Startup).s -o $(CPU0Startup).o'))
   shell(eval('$(CC) -c $(CFLAGS) $(CPU1Startup).s -o $(CPU1Startup).o'))

@target
def clean(): # <- has no dependency
    run(eval('rm -r $(BUILDdir)'))
    run(eval('rm disassembly.txt elfdump.txt dwarfinfo.txt $(executable)'))

@target
def listsrc():
  printlist(CSRC_ALL)

@target
def listobj():
  printlist(OBJ_All)

```
First of all, `makefile.py` must import pymake2. To enable detailed error messages in the build process, `Debug` variable should be set to True. The above snippet is self-explanatory to any one used to work with makefiles. 

### Features of pymake2 ###
- `makefile.py` follows similar approach of GNU make, but with the flexibility of Python
- pymake2 automatically highlights error, warning, and info messages produced by the compiler or the linker. This is especially useful when the used toolchain does not prints colorful outputs. As shown in the snippet above, to get highlighted outputs, you need to enable `HighlightErrors`, `HighlightWarnings`, and `HighlightNotes` as needed. In addition, the highlighted outputs only works with the commands provided by pymake2 such as `compile`, `link`, and `archive` and not with `shell`, `sh`, or `run` commands.
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