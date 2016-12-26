from pymake2 import *
CC = 'mips-gcc'
CObjAll = ['obj%d.o'%i for i in range(1,10)]
executable = 'out.elf'

@target
def All():
    out = sh('sfind ./ -r -f "*.o"')
    print out.split()
    # run('ls ~/ -lah')
    # for i in range(100):
    #     print('All[%d]'%i)

@target
def xxx(DependsOn = 'A'):
    for i in range(10):
        print 'Hellow [%d]'%i


@target
def xxx2 (DependsOn = 'A'):
    for i in range(10):
        print 'Hellow [%d]'%i

@target
def loop():
    sh('./loop.py')


@target
def clean():
    sh('pwd')
    sh('ll')
    sh('rm *.o')
    
@target
def clean2():
    # run('rm -f %s %s output.map elfdump.txt disassembly.txt'%(CObjAll, executable))
    cmd = eval('rm $(CObjAll) $(executable) output.map elfdump.txt disassembly.txt')
    print cmd
    run(cmd)


if __name__ == '__main__':
    xxx(DependsOn= 'B')