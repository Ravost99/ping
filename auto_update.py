import urllib, colors, os, time, config
from threading import Timer

# this took about >1 hour of coding 
# pretty much like auto `git pull`
def update(send_return=True):
  if config.debug == True:
    return
  else:
    version_update()
  # files to be updated
  stuff_to_update = ['main.py', 'auto_update.py', 'colors.py', 'templates/index.html', 'README.md']
  for item in stuff_to_update:
    new_data = ""
    update_data = ""
    # getting github repo
    data = urllib.request.urlopen("https://raw.githubusercontent.com/Ravost99/ping/master/" + item)
    for line in data.readlines():
      # to make b'<-- this' go away \/
      new_data += line.decode("utf-8")
    with open(item) as f:
      for line in f.readlines():
        update_data += line
      # you get the point...
      if new_data == update_data:
        if send_return == True:
          print(f"{colors.green}No update in {item}!{colors.reset}")
        else:
          return
      else:
        timeout = 3
        #t = Timer(timeout, print, [f'{colors.dark_red}Cancled Update in {item}{colors.reset}'])
        #t.start()
        update = input(f"There is a new update in {item}, would you like to update? You have {str(timeout)} seconds. (Will override {colors.underline}everything{colors.reset} in {item}) (Y/N) ")
        if update.lower() == 'y':
          with open(item, 'w') as file:
            file.write(new_data)
          print(f'{colors.green}Updated Successfully!{colors.reset}')
          return
        else:
          print(f"{colors.dark_red}Cancled Update in {item}{colors.reset}")
  print("Restarting...") #39 lines of _TERROR_
        

# replica of update()
def version_update():
  if config.debug == True:
    colors.rainBow("Hehe disabled =)")
  else:
    file = 'version'
    new_data = ""
    update_data = ""
    # getting github repo
    data = urllib.request.urlopen("https://raw.githubusercontent.com/Ravost99/ping/master/" + file)
    for line in data.readlines():
      
      new_data += line.decode("utf-8")
    with open(file) as f:
      for line in f.readlines():
        update_data += line
        
      if new_data == update_data:
        print(f"{colors.green}Ping version up to date! (v{update_data}){colors.reset}")
      else:
        print(f"{colors.bold}{colors.dark_red}Critical Update available!{colors.reset} Version {update_data} --> {new_data}")
        time.sleep(0.5)
        with open(file, 'w') as file:
          file.write(new_data)
        time.sleep(0.5)
        print(f'{colors.green}Updated to version {new_data} Successfully!{colors.reset}')