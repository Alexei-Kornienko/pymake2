from pymake2 import *
Debug = True
#######################################################
# Project Spesifications
# Sepecifiy the Executable output file
executable = 'out.elf'
BUILDdir = './build'
############ Specify the linker script
LikerScript = '-T lscript.ld'
#ERAPlatformDir= '/home/saud/Dropbox/pycharmProjects/ERA/compiler/ERAPlatform/'
ERAPlatformDir = eval('$(ERAPlatformDir)')
ERAsimDrivers = eval('$(ERAPlatformDir)/ERAsimDrivers')

#ERAdrivers includes
ERAIncludes = shell(eval("sfind $(ERAsimDrivers) -r -d -a"))
ERAIncludes += eval(' $(ERAsimDrivers)')

# Project Includes
# include all the directories and sub directories the project folder.
ProjIncludes = join('./', shell('sfind ./ -r -d'))

Includes = eval('$(ProjIncludes) $(ERAIncludes)').split()
Includes = ['-I %s'%item for item in Includes]
# Includes = join(Includes)

# include all the .c files in the project directory and sub directories.
CSRC_Project = shell('sfind ./ -r -f "*.c"')
CSRC_ERADrivers = shell(eval("sfind $(ERAsimDrivers) -r -f '*.c' -a"))
#CSRC_ERADriversDIRs := $(shell sfind $(ERAsimDrivers) -r -d -a)
CSRC_ALL = eval('$(CSRC_Project) $(CSRC_ERADrivers)')

OBJ_Project = replace(CSRC_Project, '.c', '.o')
OBJ_ERADrivers = replace(CSRC_ERADrivers, '.c', '.o')
# OBJ_ERADrivers := $(addprefix ERAsimDrivers/, $(OBJ_ERADrivers))
OBJ_All  = eval('$(OBJ_Project) $(OBJ_ERADrivers)').split()
OBJ_All  = replace(OBJ_All, ERAPlatformDir, '')
OBJ_All  = [BUILDdir + '/' + e for e in OBJ_All]
OBJ_All  = normpaths(OBJ_All)

pass
# #ERA Platform includes
# ERAIncludes = shell('getsrcfiles /home/saud/Dropbox/pycharmProjects/ERA/compiler/ERAPlatform/mips/ -r -d')

# # include all the directories and sub directories the project folder.
# ProjIncludes = shell('getsrcfiles ./ -r -d')
# # ProjIncludes = join(ProjIncludes, shell('getsrcfiles %s/mylibsrc/ -r -d'%ERAPlatformDir))
# ProjIncludes = join(ProjIncludes, shell(eval("getsrcfiles $(ERAPlatformDir)/mylibsrc/ -r -d")))
# ProjIncludes = ProjIncludes.split()
# ProjIncludes = ['-I %s'%item for item in ProjIncludes]
# # ProjIncludes = $(patsubst %,-I %, $(ProjIncludes))

# # include all the .c files in the project directory and sub directories.
# CSRC = shell('getsrcfiles ./ -r -f "*.c"')
# CSRC += ' ' + shell(eval("getsrcfiles $(ERAPlatformDir)/mylibsrc/ -r -f '*.c'"))
# CSRC = CSRC.split()
# CObjAll = replace(CSRC, '.c', '.o')
# IgnoredObj = ['blabla.o']
# CObj = exclude(CObjAll, IgnoredObj)
#######################################################

#######################################################
## toolchaine spesification
CC      			= 'mips-gcc'
CPU0Startup 		= 'src/CPU0'
CPU1Startup 		= 'src/CPU1'
startobj 			= 'src/CPU0.o src/CPU1.o'
# IncludePaths 		= -I$(ERAIncludes) -I$(ProjIncludes)
IncludePaths 		= Includes
LibPaths 			= '-L /home/saud/Dropbox/pycharmProjects/ERA/compiler/ERAPlatform/mips/'
CFLAGS 				= eval('-std=c99 -nostdlib -O1 -msoft-float -march=mips1 -EL -g -Wall $(IncludePaths)')
#LINKFLAGS 			= $(LikerScript) -nostdlib -ffreestanding -Xlinker -Map=output.map $(LibPaths) -lc 
LINKFLAGS 			= eval('$(LikerScript) -nostdlib -march=mips1 -ffreestanding -EL -Xlinker -Map=output.map $(LibPaths) -lc')
########################################################

################## Targets #############################
@target
def all(ObjProj):
  if link(CC, LINKFLAGS, join(startobj, OBJ_All), executable):
    run('mips-objdump -D %s > disassembly.txt'%executable)
    run('mips-readelf -a %s > elfdump.txt'%executable)
    run('mips-objdump --dwarf=info %s > dwarfinfo.txt'%executable)
    run('mips-size %s'%executable)
    return True

@target
def ObjProj(CSRC_ALL):
  if compile(CC, CFLAGS, CSRC_ALL, OBJ_All):
  # if compile(CC, CFLAGS, CSRC_ALL):
    return True
# objs: $(CObjAll)	

# startup: 
# 	$(CC) -c $(CFLAGS) $(CPU0Startup).s -o $(CPU0Startup).o
# 	$(CC) -c $(CFLAGS) $(CPU1Startup).s -o $(CPU1Startup).o

@target
def clean():
  	# run('rm -f %s %s output.map elfdump.txt disassembly.txt'%(CObjAll, executable))
	# run(eval('rm $(CObjAll) $(executable) output.map elfdump.txt disassembly.txt'))
	run(eval('rm -r $(BUILDdir)'))
	run(eval('rm disassembly.txt elfdump.txt dwarfinfo.txt $(executable)'))

@target
def listsrc():
  printlist(CSRC_ALL)

@target
def listobj():
  printlist(OBJ_All)
