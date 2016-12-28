import sys
import os
import sarge
import re
import inspect
import utility as utl

# makefileM = None # to be assigned upon importing

# reP = re.compile(r'\$\((\w+)\)')

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

def get_dir(path):
  if type(path) is str:
    dir_str = os.path.dirname(path)
    return dir_str
  elif type(path) is list:
    retPaths = []
    for p in path:
      dir_str = os.path.dirname(p)
      retPaths.append(dir_str)
    return retPaths
  else:
    return None
  
def printlist(lst):
  if type(lst) is not list:
    lst = lst.split()
  for i in lst:
    print i
  
  return lst
    
def get_filename(path):
  if type(path) is str:
    dir_str = os.path.basename(path)
    return dir_str
  elif type(path) is list:
    retPaths = []
    for p in path:
      dir_str = os.path.basename(p)
      retPaths.append(dir_str)
    return retPaths
  else:
    return None
   
  
def compile(compiler, flags, sources, objects):
  # utl.print_color('Compiling ...', utl.tty_colors.On_Cyan)
  if type(sources) is list:
    srcs = sources
  else: # in the case of str
    srcs = sources.split()
  
  if type(objects) is list:
    objs = objects
  else: # in the case of str
    objs= objects.split()

  if len(srcs) != len(objs):
    utl.write_color('Error: ', utl.tty_colors.Red)
    print 'the length of the source files list does not match with objects files list'
    return
  
  for i, item in enumerate(srcs):
    cmd = '{CC} {flags} -c {src} -o {obj}'.format(CC=compiler, flags=flags, src=item, obj=objs[i])
    
    srcFile = os.path.basename(item)
    objFile = os.path.basename(objs[i])
    srcFile = srcFile.split('.')[0]
    objFile = objFile.split('.')[0]
    if srcFile != objFile:
      utl.write_color('Compiling Error: ', utl.tty_colors.BRed)
      print 'source file %s and object file %s do not match. Make sure that the source and the object files lists are correspondent'%(item, objs[i])
      return False
    if os.path.isfile(objs[i]): # if the object file already exists
      src_mTime = os.path.getmtime(item)
      obj_mtime = os.path.getmtime(objs[i])
      if src_mTime <= obj_mtime:
        continue
    else: # no obj file exists
        objDir = os.path.dirname(objs[i])
        objDir = os.path.normpath(objDir)
        if not os.path.exists(objDir):
          os.makedirs(objDir)
    utl.print_color('Compiling: %s'%item, utl.tty_colors.On_Cyan)
    if not run(cmd, show_cmd=True):
      utl.write_color('Error: ', utl.tty_colors.BRed)
      print 'failed to compile, \n  %s'%cmd
      return False
  
  return True
    
def link(linker, flags, objects, executable):
  if type(objects) is list:
    objs = ' '.join(objects)
  else:
    objs = objects
    
  objectsList = objs.split()

  linkFlag = True
  if os.path.isfile(executable):
    linkFlag = False
    exe_mTime = os.path.getmtime(executable)
    for obj in objectsList:
      obj_mtime = os.path.getmtime(obj)
      if obj_mtime > exe_mTime:
        linkFlag = True
        break
  
  if linkFlag:
    utl.print_color('Linking ...', utl.tty_colors.On_Blue)
    cmd = '{linker} {flags} {objs} -o {executable}'.format(linker=linker, flags=flags, objs=objs, executable=executable)
    return run(cmd, show_cmd=True)
  else:
    return True
    

def normpaths(paths):
  if type(paths) is str:
    dir_str = os.path.normpath(paths)
    return dir_str
  elif type(paths) is list:
    retPaths = []
    for p in paths:
      dir_str = os.path.normpath(p)
      retPaths.append(dir_str)
    return retPaths
  else:
    return None

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
  
def run(cmd, show_cmd=False):
  if show_cmd:
    utl.print_color(cmd)
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