try:
  import requests, pytz
  from discord_webhook import DiscordWebhook, DiscordEmbed
except:
  import os
  os.system('pip install requests pytz discord_webhook')
  os.system('pip install -U pip')

import time, colors, os, time, math, random, re
if os.path.isfile('config.py'):
  import config
else:
  from setup import setup
  setup()
  os.system('python3 main.py')

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from auto_update import update, version_update
from colors import colorMsg, rainBow, allBGCodes, allColorCodes
from threading import Thread

if config.debug == True:
  def print(args):
    rainBow(args)

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
        f.write("\n"+url)
      return 'Added url: '+url

# simple file reader like in line 77, for /logs
def readFile(file:str, type:str='r'):
  lines = ''''''
  with open(file, type) as f:
    for line in f.readlines():
      lines += line + '\n'
  return lines

# get website title for discord webhook logging
def get_title(url):
  headers = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 14324.80.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.102 Safari/537.36',
  }
  try:
    req = requests.get(url, headers=headers)
    title = re.search('<title>(.*)</title>', req.text).group(1)

    return title
  except:
    return None
  
# discord webhook logging
def webhook_error(url, status, round, time, date):
  webhook = DiscordWebhook(url=os.environ['webhook'])
  title = get_title(url)
  if title is None:
    site = 'Site'
  else:
    site = title
  embed = DiscordEmbed(
    title=f'{site} is down!',
    color='ff0000'
  )
  embed.add_embed_field(
    name='Url',
    value=f'{url} ({status})'
  )
  embed.add_embed_field(
    name='Ping Round',
    value=round
  )
  embed.set_footer(
    text=f'{time} {date}'
  )
  
  webhook.add_embed(embed)
  response = webhook.execute()

def get_messages(ping_round=None):
  sites = []
  percent = 100
  with open("sites.txt") as f:
    pings = f.read().split('\n')
    length = len(pings)
    num = 100/length
    for i in pings:
      if i != '':
        headers = {
          'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 14324.80.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.102 Safari/537.36',
        }
        req = requests.get(i, headers=headers, allow_redirects=False)
        sites.append(req.status_code)
        if req.status_code == 404:
          percent -= num
    messages = [f'Almost to ping round #{str(int(math.ceil(ping_round)))}!', f'{str(ping_round*5)} is 5 times your ping round!', 'The github repo is https://github.com/Ravost99/ping', 'Hello', 'Random round messages!', f'{percent}% of your sites are up!']
    return random.choice(messages)

#tldr ping function
def ping(round:int):
  # yup all the way at the top :D
  version_update()
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
          if i != '':
            # glitch.com sites were being funny, so i just used headers
            #if 'glitch.me' in i:
              # maybe implement UserAgent headers to all sites?
            headers = {
              'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 14324.80.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.102 Safari/537.36',
            }
              #req = requests.get(i, headers=headers)
            #else:
            req = requests.get(i, headers=headers, allow_redirects=False)
            # status codes with colors!
            if req.status_code == 200 or req.status_code == 202:
              color = colors.green
            elif req.status_code == 400 or req.status_code == 401 or req.status_code == 404 or req.status_code == 502:
              # error logging
              if config.logging == True:
                # discord webhook logging
                webhook_error(i, req.status_code, str(round), current_time, current_date)
                
                with open('log.txt', 'a') as f:
                  if config.ping_rounds == True:
                    f.write(f'Errors in Ping round #{str(round)}\nError on Url {i}: \'{req.status_code}\' - {current_time} {current_date}\n')
                  else:
                    f.write(f'Error on Url {i}: \'{req.status_code}\' - {current_time} {current_date}\n')
              color = colors.dark_red
            elif req.status_code == 301  or req.status_code == 302 or req.status_code == 303 or req.status_code == 307 or req.status_code == 308:
              # redirect https://www.google.com/search?q=check+if+site+is+redirect+python
              requests.get(req.url, headers=headers)
              color = colors.yellow
            # all 500-599 are errors
            elif req.status_code.startswith(5):
              # error logging again
              if config.logging == True:
                # discord webhook logging
                webhook_error(i, req.status_code, str(round), current_time, current_date)
                
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
    requests.get(config.website, allow_redirects=False)
    # waiting for the ping interval in config.py
    time.sleep(config.ping_intvl*60)

# threading to start the web server And start pinging sites
server = Thread(target=run)
server.start()
start = Thread(target=start)
start.start()
self = Thread(target=self_ping)
self.start()