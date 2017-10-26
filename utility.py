from sys import stdout
import inspect
import traceback
import re

from time import time, sleep
class tty_colors_cmds:
  # Reset
  Color_Off='\033[0m'       # Text Reset
  
  # Regular Colors
  Black='\033[0;30m'        # Black
  Red='\033[0;31m'          # Red
  Green='\033[0;32m'        # Green
  Yellow='\033[0;33m'       # Yellow
  Blue='\033[0;34m'         # Blue
  Purple='\033[0;35m'       # Purple
  Cyan='\033[0;36m'         # Cyan
  White='\033[0;37m'        # White
  
  # Bold
  BBlack='\033[1;30m'       # Black
  BRed='\033[1;31m'         # Red
  BGreen='\033[1;32m'       # Green
  BYellow='\033[1;33m'      # Yellow
  BBlue='\033[1;34m'        # Blue
  BPurple='\033[1;35m'      # Purple
  BCyan='\033[1;36m'        # Cyan
  BWhite='\033[1;37m'       # White
  
  # Underline
  UBlack='\033[4;30m'       # Black
  URed='\033[4;31m'         # Red
  UGreen='\033[4;32m'       # Green
  UYellow='\033[4;33m'      # Yellow
  UBlue='\033[4;34m'        # Blue
  UPurple='\033[4;35m'      # Purple
  UCyan='\033[4;36m'        # Cyan
  UWhite='\033[4;37m'       # White
  
  # Background
  On_Black='\033[40m'       # Black
  On_Red='\033[41m'         # Red
  On_Green='\033[42m'       # Green
  On_Yellow='\033[43m'      # Yellow
  On_Blue='\033[44m'        # Blue
  On_Purple='\033[45m'      # Purple
  On_Cyan='\033[46m'        # Cyan
  On_White='\033[47m'       # White
  
  # High Intensity
  IBlack='\033[0;90m'       # Black
  IRed='\033[0;91m'         # Red
  IGreen='\033[0;92m'       # Green
  IYellow='\033[0;93m'      # Yellow
  IBlue='\033[0;94m'        # Blue
  IPurple='\033[0;95m'      # Purple
  ICyan='\033[0;96m'        # Cyan
  IWhite='\033[0;97m'       # White
  
  # Bold High Intensity
  BIBlack='\033[1;90m'      # Black
  BIRed='\033[1;91m'        # Red
  BIGreen='\033[1;92m'      # Green
  BIYellow='\033[1;93m'     # Yellow
  BIBlue='\033[1;94m'       # Blue
  BIPurple='\033[1;95m'     # Purple
  BICyan='\033[1;96m'       # Cyan
  BIWhite='\033[1;97m'      # White
  
  # High Intensity backgrounds
  On_IBlack='\033[0;100m'   # Black
  On_IRed='\033[0;101m'     # Red
  On_IGreen='\033[0;102m'   # Green
  On_IYellow='\033[0;103m'  # Yellow
  On_IBlue='\033[0;104m'    # Blue
  On_IPurple='\033[0;105m'  # Purple
  On_ICyan='\033[0;106m'    # Cyan
  On_IWhite='\033[0;107m'   # White


class tty_colors:
  # Reset
  Color_Off = '0'  # Text Reset
  
  # Regular Colors
  Black = '30'  # Black
  Red = '31'  # Red
  Green = '32'  # Green
  Yellow = '33'  # Yellow
  Blue = '34'  # Blue
  Purple = '35'  # Purple
  Cyan = '36'  # Cyan
  White = '37'  # White
  
  # High Intensity
  IBlack = '90'  # Black
  IRed = '91'  # Red
  IGreen = '92'  # Green
  IYellow = '93'  # Yellow
  IBlue = '94'  # Blue
  IPurple = '95'  # Purple
  ICyan = '96'  # Cyan
  IWhite = '97'  # White
  
  # Background
  On_Black = '40'  # Black
  On_Red = '41'  # Red
  On_Green = '42'  # Green
  On_Yellow = '43'  # Yellow
  On_Blue = '44'  # Blue
  On_Purple = '45'  # Purple
  On_Cyan = '46'  # Cyan
  On_White = '47'  # White
  
  # High Intensity backgrounds
  On_IBlack = '100'  # Black
  On_IRed = '101'  # Red
  On_IGreen = '102'  # Green
  On_IYellow = '103'  # Yellow
  On_IBlue = '104'  # Blue
  On_IPurple = '105'  # Purple
  On_ICyan = '106'  # Cyan
  On_IWhite = '107'  # White


def print_color(txt, color=tty_colors_cmds.Color_Off):
  out = '%s%s'%(color, txt)
  stdout.write(out)
  #reset
  stdout.write(tty_colors_cmds.Color_Off)
  stdout.write('\n')

def write_color(txt, color=tty_colors_cmds.Color_Off):
  out = '%s%s'%(color, txt)
  stdout.write(out)
  #reset
  stdout.write(tty_colors_cmds.Color_Off)

def get_colored(txt, fg_color='', bg_color='', Bold=False):
  B = '1' if Bold else '0'
  fg = fg_color if fg_color == '' else ';' + fg_color
  bg = bg_color if bg_color == '' else ';' + bg_color
  if type(txt) is unicode:
    txt = txt.encode('UTF-8')
  ttycmd = '\033[{B}{fg}{bg}m{txt}\033[0m'.format(B=B,fg=fg,bg=bg, txt=txt)
  return ttycmd
  
def tty_reset():
  stdout.write('\e[0m')

def get_regx_spans(txt, regxpattern):
  spans = []
  iterV = regxpattern.finditer(txt)
  for m in iterV.next():
    span = m.span()
    spans.append(span)
  if len(spans)> 0:
    return spans
  else:
    return None

def Highlight_custom(txt, pattern, color):
  #type:(str, re._pattern_type, tuple[str]) -> str
  if type(txt) is unicode:
    txt = txt.encode('UTF-8')
  retV = txt
  if type(pattern) is re._pattern_type:
    founds = pattern.findall(txt)
    newtxt = txt
    for s in founds:
      colored_s = get_colored(s, color[0], color[1], Bold=True)
      newtxt = newtxt.replace(s, colored_s)
    retV = newtxt
  elif type(pattern) is str:
    s = pattern
    colored_s = get_colored(s, color[0], color[1], Bold=True)
    newtxt = txt.replace(s, colored_s)
    retV = newtxt

  return retV

  # vars = re.findall(r'\$\((\w+)\)', txt)
  # newtxt = re.sub(r'\$\((\w+)\)', r'{\1}', txt)
  #
  # repWith = get_colored('Warning', tty_colors.Yellow, tty_colors.On_IBlack, Bold=True)
  # reTV = txt.replace('warning', repWith)
  # reTV = reTV.replace('Warning', repWith)
  # return reTV

def HighlightWarnings(txt):
  #type:(str) -> str

  repWith = get_colored('Warning', tty_colors.Yellow, tty_colors.On_IBlack, Bold=True)
  reTV = txt.replace('warning', repWith)
  reTV = reTV.replace('Warning', repWith)
  return reTV

def HighlightErrors(txt):
  #type:(str) -> str
  repWith = get_colored('Error', tty_colors.Red, tty_colors.On_IBlack, Bold=True)
  reTV = txt.replace('error', repWith)
  reTV = reTV.replace('Error', repWith)
  return reTV

def HighlightNotes(txt):
  #type:(str) -> str
  repWith = get_colored('Note', tty_colors.Cyan, Bold=True)
  reTV = txt.replace('note', repWith)
  reTV = reTV.replace('Note', repWith)

  repWith = get_colored('Info', tty_colors.Cyan, Bold=True)
  reTV = reTV.replace('info', repWith)
  reTV = reTV.replace('Info', repWith)

  return reTV

def get_makefile_var(var_str):
  """
  :param var_str: str
  :return:
  """
  outerframe = inspect.stack()[1][0]
  outerframe = outerframe.f_back.f_back
  outerframeGlobals = outerframe.f_globals

  try:
    var = outerframeGlobals[var_str]
    return var
  except:
    return None

def Print_Debuging_messages():
  print_color('Debugging message: (Program Exception)', tty_colors_cmds.On_Red)
  traceback.print_exc()
  
def is_Highlight_ON():
  outerframe = inspect.stack()[1][0]
  preFrame = outerframe.f_globals
  outerframe = outerframe.f_back
  outerframeGlobals = outerframe.f_globals

  try:
    Highlighting = preFrame['_Highlighting']
    if Highlighting:
      return True
  except:
    pass

  try:
    HighlightWarnings = outerframeGlobals['HighlightWarnings']
    if HighlightWarnings:
      return True
  except:
    pass
  
  try:
    HighlightErrors = outerframeGlobals['HighlightErrors']
    if HighlightErrors:
      return True
  except:
    pass
  
  try:
    HighlightNotes = outerframeGlobals['HighlightNotes']
    if HighlightNotes:
      return True
  except:
    pass

  return False

def wait_process(Timeout, Proc, Print_statusTime = -1):
  cindex = 0
  timeStep = 0.1
  sec_count = 1.0
  CountDown = Timeout
  
  T1 = time()
  tdiff = time() - T1
  while tdiff < Timeout:
    alive = Proc.poll()
    if alive is not None:
      stdout.write('\r                          \r')
      return False
    sleep(timeStep); sec_count -= timeStep
    tdiff = time() - T1
    CountDown = int(Timeout - tdiff)
    if tdiff >= Print_statusTime and sec_count <=0:
      sec_count = 1.0
      if cindex == 0:
        stdout.write('\r                          \r')
        write_color('\rwaiting... [%d]'%CountDown, tty_colors_cmds.On_Yellow); stdout.flush()
        cindex = 1
      else:
        stdout.write('\r                          \r')
        write_color('\rwaiting... [%d]'%CountDown, tty_colors_cmds.On_Cyan) ; stdout.flush()
        cindex = 0
      

  stdout.write('\r          \r')
  return True # The Process is Timed Out

def kill_alive_process(Proc):
  alive = Proc.poll()
  if alive is None:
    try:
      Proc.kill()
    except:
      pass
  