try:
  import requests, pytz
except:
  import os
  os.system('python3 -m pip install requests pytz')
  os.system('python3 -m pip install -U pip')
  import requests, pytz

import time, colors, os, time, math, random, re, logging

if os.path.isfile('config.py'):
  import config
else:
  from setup import setup
  setup()
  os.system('python3 main.py')

#disable logging in the console
if config.console_logging is not True:
  log = logging.getLogger('werkzeug')
  log.setLevel(logging.ERROR)

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from auto_update import update, version_update
from colors import colorMsg, rainBow, allBGCodes, allColorCodes
from threading import Thread, Timer

if config.debug == True:
  def print(args):
    rainBow(args)

def clear():
  os.system('clear')

app = Flask(__name__)
last_commit = requests.get('https://api.github.com/repos/Ravost99/ping').json()['pushed_at'][:0-10]

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
  if config.ping_rounds == True:
    return readFile('round')
  else:
    return 'Ping rounds are off!'

# getting logs
@app.route('/logs')
def getLogs():
  if config.logging == True:
    return readFile('log.txt')
  else:
    return 'Logging is off!'

# checking if site is up, for my iphone shortcut
@app.route('/up')
def up():
  return 'up', 200

# ------------------ Functions ------------------------#

# for quick fetch feature, will try to add rate limiting
def fetch(url):
  # using UserAgent to ping glitch sites, to prevent 401 unauthorized
  headers = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 14324.80.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.102 Safari/537.36',
  }
  if url in readFile('sites.txt'):
    req = requests.get(url, headers=headers, allow_redirects=False)
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
        f.write('\n'+url)
      return 'Added url: '+url

# simple file reader like in line 77, for /logs
def readFile(file:str, type:str='r'):
  lines = ''''''
  with open(file, type) as f:
    for line in f.readlines():
      lines += line + '\n'
  return lines

# ping url for threads
def get_ping_url(url, _print=True):
  # "commenting out" urls
  if url.startswith('#'):
    return
  
  now = datetime.now(pytz.timezone('America/Chicago'))
  current_time = now.strftime('%I:%M:%S %p')
  current_date = datetime.today().strftime('%m-%d-%Y')
  headers = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 14324.80.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.102 Safari/537.36',
  }
  req = requests.get(url, headers=headers, allow_redirects=False)
  with open('round') as f:
    round = f.read()
  
  # status codes with colors!
  if req.status_code == 200:
    color = colors.green
  elif req.status_code == 202:
    color = colors.orange
  elif req.status_code == 400 or req.status_code == 401 or req.status_code == 404 or req.status_code == 502:
    # error logging
    if config.logging == True:                
      with open('log.txt', 'a') as f:
        if config.ping_rounds == True:
          f.write(f'Errors in Ping round #{str(round)}\nError on Url {url}: \'{req.status_code}\' - {current_time} {current_date}\n')
        else:
          f.write(f'Error on Url {url}: \'{req.status_code}\' - {current_time} {current_date}\n')
    color = colors.dark_red
  # redirects
  elif req.status_code == 301  or req.status_code == 302 or req.status_code == 303 or req.status_code == 307 or req.status_code == 308:
    requests.get(req.url, headers=headers)
    color = colors.yellow
  # all 500-599 are all errors
  elif str(req.status_code).startswith('5'):
    # error logging again
    if config.logging == True:               
      with open('log.txt', 'a') as f:
        if config.ping_rounds == True:
          f.write(f'Errors in Ping round #{str(round)}\nError on Url {url}: \'{req.status_code}\' - {current_time} {current_date}\n')
        else:
          f.write(f'Error on Url {url}: \'{req.status_code}\' - {current_time} {current_date}\n')
    color = colors.purple
  else:
    color = colors.reset
    
  if _print == True:
    print(f'Pinging site: {url} ({color}{req.status_code}{colors.reset})')
  
  return req
  
# ping function with threads
def ping(round:int):
  version_update()
  clear()
  messages = ['Quick fetch coming soon!', 'Ravost99 is owner!', f'The world will end in █████', 'Currently Debugging!', f'Latest commit at: {last_commit}', f'1 = {str(round - 1)}', f'{str(random.randint(0, 1000000000))}', f'- - - > {round}', 'Should I make this in Nodejs?']
  #ping rounds
  if config.ping_rounds == True:
    with open('round', 'w') as f:
      f.write(str(round))
    print(f'Ping Round #{round} - {random.choice(messages)} \n')

  if config.roundly_updates == True:
    update(False)
  
  
  site_list = []
  
  with open('sites.txt') as file:
    sites = file.read().split('\n')

    for i in sites:
      if i not in site_list:
        try:
          if i != '':
            site = Thread(target=get_ping_url, args=[i])
            site.start()
            
        except:
          continue
        site_list.append(i) 
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
  colorMsg('Starting... ', colors.green)
  time.sleep(0.5)
  clear()
  while True:
    ping(round)
    # wait 15 seconds after ping round
    time.sleep(15)
    # add 1 to round
    round += 1

def self_ping():
  headers = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 14324.80.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.102 Safari/537.36',
  }
  while True:
    # getting the website / ip the server is running on (with headers)
    requests.get(config.website, headers=headers, allow_redirects=False)
    # waiting for the ping interval in config.py
    time.sleep(config.ping_intvl*60)

# threading to start the web server And start pinging sites
server = Thread(target=run)
server.start()
start = Thread(target=start)
start.start()
self = Thread(target=self_ping)
self.start()