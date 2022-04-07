import requests, time, colors, os, time, pytz
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from colors import colorMsg, rainBow, allBGCodes, allColorCodes
from threading import Thread

def clear():
  time.sleep(0.5)
  os.system('clear')

# #2?
def clear1():
  os.system('clear')

app = Flask(__name__)

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

@app.route('/round')
def getRound():
  return readFile('round')

@app.route('/logs')
def getLogs():
  return readFile('log.txt')

@app.route('/up')
def up():
  return 'up', 200

def new(url):
  with open('sites.txt') as sites:
    if url in sites.read():
      return 'Site already added'
    else:
      with open('sites.txt', 'a') as f:
        f.write("\n"+url)
      return 'Added url: '+url

def readFile(file:str, type:str='r'):
  lines = ''''''
  with open(file, type) as f:
    for line in f.readlines():
      lines += line + '\n'
  return lines
    
#running site
def run():
  app.run(host='0.0.0.0',port=8080)

#tldr ping function
def ping(round:int):
  with open('round', 'w') as f:
    f.write(str(round))
  clear1()
  tz = pytz.timezone('America/Chicago')
  now = datetime.now(tz)
  current_time = now.strftime("%I:%M:%S %p")
  current_date = datetime.today().strftime('%m-%d-%Y')
  lst = []
  with open("sites.txt") as f:
    pings = f.read().split('\n')
    print(f"Ping round #{str(round)}")
    for i in pings:
      if i not in lst:
        try:
          if i != '':
            req = requests.get(i)
            if req.status_code == 200 or req.status_code == 302 or req.status_code == 304:
              color = colors.green
            elif req.status_code == 400 or req.status_code == 401 or req.status_code == 404:
              with open('log.txt', 'a') as f:
                f.write(f'Errors in Ping round #{str(round)}\nError on Url {i}: \'{req.status_code}\' - {current_time} {current_date}\n')
              color = colors.dark_red
            elif req.status_code == 307 or req.status_code == 308:
              color = colors.yellow
            elif req.status_code == 500:
              with open('log.txt', 'a') as f:
                f.write(f'Errors in Ping round #{str(round)}\nError on Url {i}: \'{req.status_code}\' - {current_time} {current_date}\n')
              color = colors.purple
            else:
              color = colors.reset
            print(f"Pinging site: {i} ({color}{req.status_code}{colors.reset})")
        except:
          continue
        lst.append(i)
    round += 1
    #print(pings)

def start():
  with open('round') as f:
    round = int(f.read())
  print("Starting ....")
  clear()
  while True:
    ping(round)
    time.sleep(15)
    round += 1

server = Thread(target=run)
server.start()
start = Thread(target=start)
start.start()