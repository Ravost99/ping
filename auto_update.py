import urllib, colors, os

def update():
  stuff_to_update = ['main.py', 'colors.py', 'templates/index.html', 'README.md', 'setup.py', 'auto_update.py']
  for item in stuff_to_update:
    dat = urllib.request.urlopen("https://raw.githubusercontent.com/Ravost99/ping/master/" + item).read()
    with open(item) as f:
      if dat == f.read():
        return
      else:
        update = input(f"There is a new update in {item}, would you like to update? (Will override {colors.underline}everything{colors.reset} in {item}) (Y/N) ")
        if update.lower() == 'y':
          with open(item, 'wb') as file:
            file.write(dat)
          print(f'{colors.green}Updated Successfull!{colors.reset}')
        else:
          print(f"{colors.dark_red}Cancled Update in {item}{colors.reset}")
  print("Restarting...")