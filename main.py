try:
  import requests, pytz
except:
  import os
  os.system('pip install requests pytz')
  os.system('pip install -U pip')

import time, colors, os, time
if os.path.isfile('config.py'):
  import config
else:
  from setup import setup
  setup()
  os.system('python3 main.py')

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from auto_update import update
from colors import colorMsg, rainBow, allBGCodes, allColorCodes
from threading import Thread

def clear():
  os.system('clear')

app = Flask(__name__)

# main page for ws 'POST' for adding urls
@app.route('/', methods=['POST', 'GET'])
def home():
  if request.method == 'POST':
    url = request.form['url']
    if 'http' in url:
      new(url)
    else:
      new('https://'+url)
    return render_template('index.html', url=url)
  else:
    return render_template('index.html')
  #return "<h1>Hello world!<br>Ping!</h1><br><p>Add site <a href='https://ping.ravost.repl.co/add/'>Here</a>"

# coming soon, will add a quick ping to see status
# beta code ↓
@app.route('/get/<url>', methods=['POST', 'GET'])
def get(url):
  #if request.method == "POST":
    #url = request.form['url']
    if 'http' in url:
      return fetch(url)
    else:
      return fetch('https://'+url)

# getting current round with ws instead of console
@app.route('/round')
def getRound():
  return readFile('round')

# getting logs
@app.route('/logs')
def getLogs():
  if config.logging == True:
    return readFile('log.txt')
  else:
    return 'logging is off!'

# checking if site is up, for my iphone shortcut
@app.route('/up')
def up():
  return 'up', 200

# for quick fetch feature, will try to add rate limiting
def fetch(url):
  # using UserAgent to ping glitch sites, to prevent 401 unauthorized
  headers = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 14324.80.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.102 Safari/537.36',
  }
  if url in readFile('sites.txt'):
    req = requests.get(url, headers=headers)
    return str(req.status_code)
  else:
    return 'url is not in sites.txt'

# adding new url, cant add i/o in ws functions
def new(url):
  with open('sites.txt') as sites:
    if url in sites.read():
      return 'Site already added'
    else:
      with open('sites.txt', 'a') as f:
        f.write("\n"+url)
      return 'Added url: '+url

# simple file reader like in line 77, for /logs
def readFile(file:str, type:str='r'):
  lines = ''''''
  with open(file, type) as f:
    for line in f.readlines():
      lines += line + '\n'
  return lines

#tldr ping function
def ping(round:int):
  if config.ping_rounds == True:
    with open('round', 'w') as f:
      f.write(str(round))
  if config.roundly_updates == True:
    update(False)
  clear()
  # time and date for log
  now = datetime.now(pytz.timezone('America/Chicago'))
  current_time = now.strftime("%I:%M:%S %p")
  current_date = datetime.today().strftime('%m-%d-%Y')
  # ping list
  ping_list = []
  # getting all sites in 'sites.txt'
  with open("sites.txt") as f:
    pings = f.read().split('\n')
    if config.ping_rounds == True:
      print(f"Ping round #{str(round)}")
    for i in pings:
      if i not in ping_list:
        try:
          if i.startswith('#'):
            i += 1
          if i != '':
            # glitch.com sites were being funny, so i just used headers
            #if 'glitch.me' in i:
              # maybe implement UserAgent headers to all sites?
            headers = {
              'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 14324.80.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.102 Safari/537.36',
            }
              #req = requests.get(i, headers=headers)
            #else:
            req = requests.get(i, headers=headers)
            # status codes with colors!
            if req.status_code == 200 or req.status_code == 202 or req.status_code == 302 or req.status_code == 304:
              color = colors.green
            elif req.status_code == 400 or req.status_code == 401 or req.status_code == 404 or req.status_code == 502:
              # error logging
              if config.logging == True:
                with open('log.txt', 'a') as f:
                  if config.ping_rounds == True:
                    f.write(f'Errors in Ping round #{str(round)}\nError on Url {i}: \'{req.status_code}\' - {current_time} {current_date}\n')
                  else:
                    f.write(f'Error on Url {i}: \'{req.status_code}\' - {current_time} {current_date}\n')
              color = colors.dark_red
            elif req.status_code == 307 or req.status_code == 308:
              color = colors.yellow
            elif req.status_code.startswith(5):
              # error logging again
              if config.logging == True:
                with open('log.txt', 'a') as f:
                  if config.ping_rounds == True:
                    f.write(f'Errors in Ping round #{str(round)}\nError on Url {i}: \'{req.status_code}\' - {current_time} {current_date}\n')
                  else:
                    f.write(f'Error on Url {i}: \'{req.status_code}\' - {current_time} {current_date}\n')
              color = colors.purple
            else:
              color = colors.reset
            print(f"Pinging site: {i} ({color}{req.status_code}{colors.reset})")
        except:
          continue
        ping_list.append(i)
    # next round!
    round += 1

#running ws for thread
def run():
  app.run(host='0.0.0.0',port=8080)

# start pinging
def start():
  update()
  if config.ping_rounds == True:
    # to continue with rounds in 'round'
    if os.path.isfile('round') == False:
      with open('round', 'w+') as f:
        f.write('0')
    with open('round') as f:
      round = int(f.read())
  else:
    round = 0
  colorMsg("Starting... ", colors.green)
  time.sleep(0.5)
  clear()
  while True:
    ping(round)
    # wait 15 seconds after ping round
    time.sleep(15)
    # add 1 to round
    round += 1

def self_ping():
  while True:
    # getting the website / ip the server is running on
    requests.get(config.website)
    # waiting for the ping interval in config.py
    time.sleep(config.ping_intvl*60)

# threading to start the web server And start pinging sites
server = Thread(target=run)
server.start()
start = Thread(target=start)
start.start()
self = Thread(target=self_ping)
self.start()