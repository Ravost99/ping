import os, time

def setup():
  
  logging = input("Do you want logging? (Y/N)\n")
  rounds = input("Do you want ping rounds (Y/N)\n")
  updates = input("Check for updates every round? (Will not ping until you update) (Y/N)\n")
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
    f.write(f'setup = True\nlogging = {logging}\nping_rounds = {rounds}\nroundly_updates = {updates}\nping_intvl = {interval}\nwebsite = \'{website}\'\n')
  os.remove('setup.py')