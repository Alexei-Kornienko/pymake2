__author__ = 'Saud Wasly'

import sys
import os
import sarge
import re
import inspect
import utility as util
from utility import tty_colors as colors
import fnmatch

from time import sleep
# makefileM = None # to be assigned upon importing

_Highlighting = False
_HighlightingDict = {}


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

def regx(pattern):
  retV = re.compile(pattern, flags=re.IGNORECASE)
  return retV

def hl(regxP, fg_color=colors.Yellow, bg_color = ''):
  global _Highlighting, _HighlightingDict
  _Highlighting = True
  _HighlightingDict[regxP] = (fg_color, bg_color)


def _Highlight_Outputs(txt):
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


  try: #custom highlight

    if _Highlighting:
      for key in _HighlightingDict.keys():
        color = _HighlightingDict[key]
        retV = util.Highlight_custom(retV, key, color)
  except Exception as e:
    print e
    pass

  return retV

def find(root='./', filter='*', recursive = False, abslute = False, DirOnly = False):
  srcfiles = []
  rootdir = os.path.abspath(root) if abslute else os.path.normpath(root)
  if recursive:
    for cur_root, dir, files in os.walk(rootdir):
      if DirOnly:
        srcfiles.extend([cur_root + '/' + e for e in dir])
      else:
        for srcfile in fnmatch.filter(files, filter):
          srcfiles.append(cur_root + '/' + srcfile)
  else:
    for cur_root, dir, files in os.walk(rootdir):
      if DirOnly:
        srcfiles.extend([cur_root + '/' + e for e in dir])
      else:
        for srcfile in fnmatch.filter(files, filter):
          srcfiles.append(cur_root + '/' + srcfile)
      break

  if DirOnly:
    # add the current root directory to the list
    rootdir = os.path.abspath(root) if abslute else os.path.normpath(root)
    srcfiles.append(rootdir)
  return srcfiles


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
      print(_Highlight_Outputs(outputs))
      
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
    objs = objects.strip().strip('\n')
    
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
      print(_Highlight_Outputs(outputs))
    
    if not success:
      util.print_color("Failed to link object files to assemble '%s'"%executable, util.tty_colors_cmds.BRed)
      return False
    else:
      return True
  else:
    return True
  
def archive(archiver, flags, objects, library):
  if type(objects) is list:
    objs = ' '.join(objects)
  else:
    objs = objects
    
  objectsList = objs.split()

  satisfactionFlag = False
  if os.path.isfile(library):
    satisfactionFlag = True
    output_mTime = os.path.getmtime(library)
    for obj in objectsList:
      obj_mtime = os.path.getmtime(obj)
      if obj_mtime > output_mTime:
        satisfactionFlag = False
        break
  
  if not satisfactionFlag:
    util.print_color('Archiving...', util.tty_colors_cmds.On_Blue)
    cmd = '{AR} {flags} {output} {objs}'.format(AR=archiver, flags=flags, objs=objs, output=library)
    hl = util.is_Highlight_ON()
    success, outputs = sh(cmd, True, hl)
    if hl:
      print(_Highlight_Outputs(outputs))
    
    if not success:
      util.print_color("Failed to archive object files to assemble '%s'" % library, util.tty_colors_cmds.BRed)
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

def retarget(srclist, targetP, omit=''):
  if targetP.endswith('/'):
    targetP = targetP[:-1]

  if type(srclist) is list:
    retV = []
    for item in srclist:
      x = item.replace(omit, '')
      x = targetP + '/' + x
      x = os.path.normpath(x)
      retV.append(x)

    return retV
  else:
    x = srclist.replace(omit, '')
    x = targetP + '/' + x
    x = os.path.normpath(x)
    retV = x
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

def sh(cmd, show_cmd=False, CaptureOutput = False, Timeout = -1):
  if show_cmd:
    print(cmd)
  try:
    if CaptureOutput:
      if Timeout > -1:
        P = sarge.run(cmd, shell=True, stdout=sarge.Capture(), stderr=sarge.Capture(), async=True)
        # sleep(3)
        try:
          CMD = P.commands[0] #type: sarge.Command # FIXME: This line generates index exception sometime
          timed_out = util.wait_process(Timeout, CMD)
          if timed_out:
            util.print_color('The command "%s" is timed out!'%cmd, util.tty_colors_cmds.On_Red)
          util.kill_alive_process(CMD)
        except:
          pass
      else:
        P = sarge.run(cmd, shell=True, stdout=sarge.Capture(), stderr=sarge.Capture())
    else:
      if Timeout > -1:
        P = sarge.run(cmd, shell=True, async=True)
        # sleep(3)
        try:
          CMD = P.commands[0] #type: sarge.Command # FIXME: This line generates index exception sometime
          timed_out = util.wait_process(Timeout, CMD)
          if timed_out:
            util.print_color('The command "%s" is timed out!'%cmd, util.tty_colors_cmds.On_Red)
          util.kill_alive_process(CMD)
        except:
          pass
      else:
        P = sarge.run(cmd, shell=True)
    
    outputs = ''

    if P.stdout and len(P.stdout.text) > 0:
      outputs = P.stdout.text
    if P.stderr and len(P.stderr.text) > 0:
      if outputs == '':
        outputs = P.stderr.text
      else:
        outputs += '\n' + P.stderr.text
    return P.returncode == 0, outputs
  except:
    if util.get_makefile_var('Debug') == True:
      util.Print_Debuging_messages()
  
    return False, ''
    
  
  
def run(cmd, show_cmd=False, Highlight=False, Timeout = 10):
  """
  :param cmd: (str) the shell command
  :param show_cmd: (bool) print the command before executing it
  :param Highlight: (bool) apply color highlights for the outputs
  :param Timeout: (float) any positive number in seconds
  :return:
  """
  if Highlight:
    success, outputs = sh(cmd, show_cmd, True, Timeout)
    hl_out = _Highlight_Outputs(outputs)
    print(hl_out)
  else:
    success, outputs = sh(cmd, show_cmd, False, Timeout)
  
  return success

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


if __name__ == '__main__':
    print 'testing find()'
    flist = find(DirOnly=True, abslute=False)
    printlist(flist)
    print 'File List has %d items'%len(flist)