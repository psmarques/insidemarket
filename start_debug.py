import subprocess
import sys
import requests
import json 
import time
from core.constant import TOKEN

p = subprocess.Popen(["start", "c:\\util\\ngrok\\ngrok.exe", "http", "8000"], shell=True)
time.sleep(3)

ret = requests.get('http://localhost:4040/api/tunnels')

jret = json.loads(ret.content.strip())
url = jret['tunnels'][0]['public_url']
url = url.replace("http://", "https://")
urlComp = 'https://api.telegram.org/bot{0}/setWebhook?url={1}/event/'.format(TOKEN, url)
print(urlComp)

p = subprocess.Popen(["start", "python", "manage.py", "runserver"], shell=True)

hookResult = requests.get(urlComp, timeout=5)
print(hookResult.content)

print("Ok")
