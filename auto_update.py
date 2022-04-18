import urllib, colors, os

# this took about >1 hour of coding 
# pretty much like auto `git pull`
def update():
  # files to be updated
  stuff_to_update = ['main.py', 'setup.py', 'auto_update.py', 'colors.py', 'templates/index.html', 'README.md']
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
        print(f"{colors.green}No update in {item}!{colors.reset}")
      else:
        update = input(f"There is a new update in {item}, would you like to update? (Will override {colors.underline}everything{colors.reset} in {item}) (Y/N) ")
        if update.lower() == 'y':
          with open(item, 'w') as file:
            file.write(new_data)
          print(f'{colors.green}Updated Successfull!{colors.reset}')
        else:
          print(f"{colors.dark_red}Cancled Update in {item}{colors.reset}")
  print("Restarting...") #30 lines of _TERROR_