import sys
import os
import sarge
import re
import inspect
import utility as utl

makefileM = None # to be assigned upon importing

reP = re.compile(r'\$\((\w+)\)')

def eval(txt):
  outerframe = inspect.stack()[1][0]
  outerframeGlobals = outerframe.f_globals
  
  vars = re.findall(r'\$\((\w+)\)', txt)
  newtxt = re.sub(r'\$\((\w+)\)', r'{\1}', txt)
  
  for v in vars:
    try:
      val = outerframeGlobals[v]
      if type(val) is list:
        val = ' '.join(val)
      newtxt = newtxt.replace('{%s}'%v, val)
    except:
      val = os.getenv(v)
      if val:
        newtxt = newtxt.replace('{%s}' % v, val)
      else:
        utl.print_color('Error: cannot find variable %s'% v, utl.tty_colors.Red)
        sys.exit()
  return newtxt
  
def compile(compiler, flags, sources, objects=None, buildroot=None):
  utl.print_color('Compiling ...', utl.tty_colors.On_Cyan)
  if type(sources) is list:
    srcs = sources
  else: # in the case of str
    srcs = sources.split()
  
  if not objects:
    objects = replace(srcs, '.c', '.o')
  if type(objects) is list:
    objs = objects
  else: # in the case of str
    objs= objects.split()

  if len(srcs) != len(objs):
    utl.write_color('Error: ', utl.tty_colors.Red)
    print 'the length of the source files list does not match with objects files required'
    return
  
  for i, item in enumerate(srcs):
    if buildroot:
      cmd = '{CC} {flags} -c {src} -o {broot}/{obj}'.format(CC=compiler, flags=flags, src=item, broot=buildroot, obj=objs[i])
    else:
      cmd = '{CC} {flags} -c {src} -o {obj}'.format(CC=compiler, flags=flags, src=item, obj=objs[i])
    
    if os.path.isfile(objs[i]):
      src_mTime = os.path.getmtime(item)
      obj_mtime = os.path.getmtime(objs[i])
      if src_mTime <= obj_mtime:
        continue
    else: # no obj file exists
        objDir = os.path.dirname(objs[i])
        if not buildroot:
          buildroot = os.path.relpath('./')
        objDir = os.path.relpath(objDir, buildroot)
        if not os.path.exists(objDir):
          os.makedirs(objDir)
    if not run(cmd):
      utl.write_color('Error: ', utl.tty_colors.BRed)
      print 'failed to compile, \n  %s'%cmd
      return False
  
  return True
    
def link(linker, flags, objects, executable):
  utl.print_color('Linking ...', utl.tty_colors.On_Blue)
  if type(objects) is list:
    objs = ' '.join(objects)
  else:
    objs = objects
    
  cmd = '{linker} {flags} {objs} -o {executable}'.format(linker=linker, flags=flags, objs=objs, executable=executable)
  return run(cmd)

def join(*args):
    try:
      retV = ' '.join(args) # this works if all args are str type
      return retV
    except: # deal with different types
      retV = ''
      for arg in args:
        if type(arg) is list:
          argItems = ' '.join(arg)
          retV += argItems + ' '
            
        else: # assume str
          retV += arg + ' '
      return retV
      
def replace(srclist, term, repwith):
  if type(srclist) is list:
    retV = []
    for item in srclist:
      x = item.replace(term, repwith)
      retV.append(x)
    
    return retV
  else:
    retV = srclist.replace(term, repwith)
    return retV

def exclude(original, ignors):
  retV = []
  for item in original:
    if item not in ignors:
      retV.append(item)
  return retV
      
def shell(cmd):
  P = sarge.run(cmd, shell=True, stdout=sarge.Capture())
  return P.stdout.text

def sh(cmd):
  P = sarge.run(cmd, shell=True, stdout=sarge.Capture())
  return P.stdout.text
  # out = commands.getoutput(cmd)
  # out = pexpect.run(cmd, cwd='./')
  # cmd2 = "sh -c '%s'" % cmd
  # out = pexpect.run(cmd2)
  # out = sarge.run(cmd2)
  # out = sarge.run(cmd, shell=True)
  # out = sarge.run(cmd, shell=True, async=True)
  # sys.exit()
  # sys.stdout.write(out)
  # subc = SubCommand(cmd, WorkingDirectory='./')
  
def run(cmd):
  retV = sarge.run(cmd, shell=True)
  # retV = sarge.run('ls -lah', shell=True)
  return retV.returncode == 0

def target(func):
  """
    This is a decorator function
  :param func:
  :return:
  """
  def target_func(*original_args, **original_kwargs):
    # print 'before the func'
    # print original_kwargs
    retV =  func(*original_args, **original_kwargs)
    if retV is None or retV == False:
      return False
    else:
      return True
    # print 'after the func'
  
  return target_func