import os, time

logging = input("Do you want logging? (Y/N)\n")
rounds = input("Do you want ping rounds (Y/N)\n")
updates = input("Check for updates every round? (Y/N)\n")
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
    with open('file', 'w+') as f:
      f.write('')

check('log.txt')
check('sites.txt')

print("Setup Completed!")
print("Restarting with main.py")
time.sleep(2)
with open('config.py', 'a') as f:
  f.write(f'setup = True\nlogging = {logging}\nping_rounds = {rounds}\nroundly_updates = {updates}')
os.remove(__file__)
os.system('python3 main.py')