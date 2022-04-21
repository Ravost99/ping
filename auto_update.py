import urllib, colors, os

# this took about >1 hour of coding 
# pretty much like auto `git pull`
def update(send_return=True):
  # files to be updated
  stuff_to_update = ['main.py', 'auto_update.py', 'colors.py', 'templates/index.html', 'README.md', 'version'] #version always last!
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
      # you get the point
      if new_data == update_data:
        if send_return == True:
          print(f"{colors.green}No update in {item}!{colors.reset}")
        else:
          return
      else:
        if item == 'version':
          print(f"{colors.bold}{colors.dark_red}Critical Update available!{colors.reset} Version {update_data}->{new_data}")
          with open(item, 'w') as file:
            file.write(new_data)
          print(f"{colors.green}Updated Succesfully!{colors.reset}")
        update = input(f"There is a new update in {item}, would you like to update? (Will override {colors.underline}everything{colors.reset} in {item}) (Y/N) ")
        if update.lower() == 'y':
          with open(item, 'w') as file:
            file.write(new_data)
          print(f'{colors.green}Updated to version {new_data} Successfully!{colors.reset}')
          continue
        else:
          print(f"{colors.dark_red}Cancled Update in {item}{colors.reset}")
  print("Restarting...") #39 lines of _TERROR_