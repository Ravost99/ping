import urllib, colors, os

def update():
  stuff_to_update = ['main.py', 'colors.py', 'templates/index.html', 'README.md', 'setup.py', 'auto_update.py']
  for item in stuff_to_update:
    dat = urllib.request.urlopen("https://raw.githubusercontent.com/Ravost99/ping/master/" + item).read()
    with open(item, 'wb') as file:
      file.write(dat)
  print(f'{colors.green}Updated Successfull!')
  os.system('python3 main.py')