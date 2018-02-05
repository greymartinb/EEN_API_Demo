import simplejson
from pprint import pprint
import requests
import simplejson
import json
from datetime import datetime, timedelta
from time import sleep
import os


USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
API_KEY = os.environ.get('API_KEY')

auth = {"Authentication": API_KEY}

def authenticate(USERNAME,PASSWORD,auth):
	url = "https://login.eagleeyenetworks.com/g/aaa/authenticate"
	login = {"username": USERNAME, "password": PASSWORD}
	auth = {"Authentication": API_KEY}
	global resp
	resp = requests.post(url, data=login, headers=auth)
	token = simplejson.loads(resp.content)
	return token

def authorize(token,auth):
	url = "https://login.eagleeyenetworks.com/g/aaa/authorize"	
	global resp
	resp = requests.post(url, data=token, headers=auth)
	cookie= resp.cookies
	return cookie

def listDevices(cookie,auth):
	url="https://login.eagleeyenetworks.com/g/device/list"
	global resp
	resp = requests.get(url, headers=auth, cookies=cookie)
	devices = simplejson.loads(resp.content)
	return devices

if __name__ == "__main__":
		token = authenticate(USERNAME,PASSWORD,auth)
		if resp.status_code == 200:
			cookie = authorize(token, auth)
			if resp.status_code == 200:
				devices=listDevices(cookie,auth)
				camera = devices[0][1]
				if resp.status_code == 200:
					i=1
					while i !=11:
							pprint(i)
							url = "https://c001.eagleeyenetworks.com/asset/asset/image.jpeg?"
							# date = datetime.now().strftime("%Y%m%d%H%M%S.%f")
							date= "now"
							data= {"c":camera, "t":date, "a":"all", "q":"high"}
							resp = requests.get(url,params=data, headers=auth, cookies=cookie)
							pprint(resp)
							if resp.status_code == 200:
								with open("images/preview"+str(i)+".jpg", 'wb') as f:
									sleep(1.0)
									i+=1
									for chunk in resp:
										f.write(chunk)