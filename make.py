__author__ = 'Saud Wasly'

import sys
import os
import sarge
import re
import inspect
import utility as util
 
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
        util.print_color('Error: cannot find variable %s' % v, util.tty_colors_cmds.Red)
        sys.exit()
  return newtxt

def printcolor(txt, fg='', bg='', B=False):
  msg = util.get_colored(txt, fg, bg, B)
  print msg
def Highlight_Outputs(txt):
  outerframe = inspect.stack()[1][0]
  outerframe = outerframe.f_back
  outerframeGlobals = outerframe.f_globals

  retV = txt
  try:
    HighlightWarnings = outerframeGlobals['HighlightWarnings']
    if HighlightWarnings:
      retV = util.HighlightWarnings(retV)
  except:
    pass

  try:
    HighlightErrors = outerframeGlobals['HighlightErrors']
    if HighlightErrors:
      retV = util.HighlightErrors(retV)
  except:
    pass

  try:
    HighlightNotes = outerframeGlobals['HighlightNotes']
    if HighlightNotes:
      retV = util.HighlightNotes(retV)
  except:
    pass

  return retV


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
  Highlight_NO = True if util.is_Highlight_ON() else False
    
  if type(sources) is list:
    srcs = sources
  else: # in the case of str
    srcs = sources.split()
  
  if type(objects) is list:
    objs = objects
  else: # in the case of str
    objs= objects.split()

  if len(srcs) != len(objs):
    util.write_color('Error: ', util.tty_colors_cmds.Red)
    print 'the length of the source files list does not match with objects files list'
    return
  
  for i, item in enumerate(srcs):
    cmd = '{CC} {flags} -c {src} -o {obj}'.format(CC=compiler, flags=flags, src=item, obj=objs[i])
    
    srcFile = os.path.basename(item)
    objFile = os.path.basename(objs[i])
    srcFile = srcFile.split('.')[0]
    objFile = objFile.split('.')[0]
    if srcFile != objFile:
      util.write_color('Compiling Error: ', util.tty_colors_cmds.BRed)
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
   
    util.print_color('Compiling: %s' % item, util.tty_colors_cmds.On_Cyan)
    success, outputs = sh(cmd, True, Highlight_NO)
    if Highlight_NO:
      print(Highlight_Outputs(outputs))
      
    if not success:
    # if not run(cmd, show_cmd=True):
      util.write_color('Error: ', util.tty_colors_cmds.BRed)
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
    util.print_color('Linking ...', util.tty_colors_cmds.On_Blue)
    cmd = '{linker} {flags} {objs} -o {executable}'.format(linker=linker, flags=flags, objs=objs, executable=executable)
    hl = util.is_Highlight_ON()
    success, outputs = sh(cmd, True, hl)
    if hl:
      print(Highlight_Outputs(outputs))
    
    if not success:
      util.print_color("Failed to link object files to assemble '%s'"%executable, util.tty_colors_cmds.BRed)
      return False
    else:
      return True
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

def sh(cmd, show_cmd=False, CaptureOutput = True):
  if show_cmd:
    print(cmd)

  if CaptureOutput:
    P = sarge.run(cmd, shell=True, stdout=sarge.Capture(), stderr=sarge.Capture())
  else:
    P = sarge.run(cmd, shell=True)
  
  outputs = ''
  if len(P.stdout.text) > 0:
    outputs = P.stdout.text
  if len(P.stderr.text) > 0:
    if outputs == '':
      outputs = P.stderr.text
    else:
      outputs += '\n' + P.stderr.text
      
  return P.returncode==0, outputs
  
def run(cmd, show_cmd=False):
  if show_cmd:
    print(cmd)
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