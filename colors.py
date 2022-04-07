import random, sys

#main colors
white= "\u001b[38;2;255;255;255m"
tan = "\u001b[38;2;189;189;78m"
brown= "\u001b[38;2;139;69;19m"
cyan= "\u001b[38;2;0;255;255m"
green= "\u001b[38;2;0;128;0m"
orange= "\u001b[38;2;255;128;0m"
blue= "\u001b[38;2;0;0;255m"
pink= "\u001b[38;2;255;0;255m"
purple= "\u001b[38;2;127;0;255m"
darkcyan= "\u001b[38;2;0;204;204m"
yellow= "\u001b[38;2;255;255;0m"
red= "\u001b[38;2;255;0;0m"
dark_red = "\u001b[38;2;153;0;0m"
black= "\u001b[38;2;0;0;0m"
magenta= "\u001b[38;2;255;0;255m"
lime= "\u001b[38;2;0;255;0m"
gray = "\u001b[38;2;128;128;128m"

#styles
bold= "\033[1m"
underline= "\033[4m"
reset= "\033[0m"
none = reset

#backgrounds
bg_none= '\x1b[0m'
bg_white= "\u001b[48;2;255;255;255m"
bg_tan = "\u001b[48;2;189;189;78m"
bg_brown= "\u001b[48;2;139;69;19m"
bg_cyan= "\u001b[48;2;0;255;255m"
bg_green= "\u001b[48;2;0;128;0m"
bg_orange= "\u001b[48;2;255;128;0m"
bg_blue= "\u001b[48;2;0;0;255m"
bg_pink= "\u001b[48;2;255;0;255m"
bg_purple= "\u001b[48;2;127;0;255m"
bg_darkcyan= "\u001b[48;2;0;204;204m"
bg_yellow= "\u001b[48;2;255;255;0m"
bg_red= "\u001b[48;2;255;0;0m"
bg_dark_red = "\u001b[48;2;153;0;0m"
bg_black= "\u001b[48;2;0;0;0m"
bg_magenta= "\u001b[48;2;255;0;255m"
bg_lime= "\u001b[48;2;0;255;0m"
bg_gray = "\u001b[48;2;128;128;128m"

#\u001b[48;5; means bg
#\u001b[38;5; means text color

def colorMsg(msg, color, background=bg_none):
  try:
    print(f"{background}{color}{msg}{reset}")
  except AttributeError:
    quit(f'color not found "{color}"')

def rainBow(msg):
  allColors = [white, tan, brown, cyan, green, orange, blue, pink, purple, darkcyan, red, yellow, dark_red, black, magenta, lime, gray]

  allBGColors = [bg_white, bg_tan, bg_brown, bg_cyan, bg_green, bg_orange, bg_blue, bg_pink, bg_purple, bg_darkcyan, bg_red, bg_yellow, bg_dark_red, bg_black, bg_magenta, bg_lime, bg_gray]

  allStyles = [bold, underline, reset]

  #message
  for i in range(len(msg)):
    #pick and message
    color = random.choice(allColors)
    bg = random.choice(allBGColors)
    style = random.choice(allStyles)
    sys.stdout.write(f"{color}{bg}{style}{msg[i]}")
  print(reset)

def allBGCodes():
  for i in range(0, 16):
    for j in range(0, 16):
        code = str(i * 16 + j)
        sys.stdout.write(u"\u001b[48;5;" + code + "m " + code.ljust(4))
    print(u"\u001b[0m")

def allColorCodes():
  for i in range(0, 16):
      for j in range(0, 16):
          code = str(i * 16 + j)
          sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
      print(u"\u001b[0m")