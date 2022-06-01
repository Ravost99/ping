import os, time

def setup():
  
  logging = input("Do you want logging? (Y/N)\n")
  rounds = input("Do you want ping rounds (Y/N)\n")
  updates = input("Check for updates every round? (Will not ping until you update) (Y/N)\n")
  console_logging = input("Do you want logging in the console? (Won't Print something like this :\n'172.18.0.1 - - [15/May/2022 22:18:11] \"GET / HTTP/1.1\" 200 -')\n(Y/N)\n")
  website = input("Enter the website or ip address the pinger is running on:\n")
  interval = int(input("What do you want the self-ping interval to be? (minimum 5) (in minutes)\n"))
  
  
  if logging.lower() == 'y':
    logging = True
  else:
    logging = False
  
  if rounds.lower() == 'y':
    rounds = True
  else:
    rounds = False
  
  if updates.lower() == 'y':
    updates = True
  else:
    updates = False

  if console_logging.lower() == 'y':
    console_logging = True
  else:
    console_logging = False
  
  def check(file):
    if os.path.isfile(file) == True:
      return
    else:
      with open(file, 'w+') as f:
        f.write('')
  
  check('log.txt')
  check('sites.txt')
  
  print("Setup Completed!")
  print("Restarting with main.py")
  time.sleep(2)
  with open('config.py', 'a') as f:
    f.write(f'setup = True\nlogging = {logging}\nconsole_logging = {console_logging}\nping_rounds = {rounds}\nroundly_updates = {updates}\nping_intvl = {interval}\nwebsite = \'{website}\'\ndebug = False\n')
  removed_files = ['setup.py', '.github', '.gitignore']
  for item in removed_files:
    os.remove(item)