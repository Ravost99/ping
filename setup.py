import os, time

logging = input("Do you want logging?")

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
os.remove(__file__)
os.system('python3 main.py')