import win10toast
import requests
import time

from res.modules.tr_fl import conv
from jsonc_parser.parser import JsoncParser

cookie = JsoncParser.parse_file('./cookie.jsonc').get("cookie")
config = JsoncParser.parse_file('./config.jsonc')

API_URL = "https://privatemessages.roblox.com/v1/messages/unread/count"

def notify():
    toast = win10toast.ToastNotifier()
    toast.show_toast(config.get("onMessage")["title"], config.get("onMessage")["content"], duration = config.get("onMessage")["duration"], icon_path="./res/icons/icon.ico", threaded=True, sound=False)

while True:
	urlHandler = requests.get(API_URL,
	    headers = {"content-type": "application/json"},
	    cookies = {'.ROBLOSECURITY': cookie}
	)

	result = urlHandler.json()
	
	if result != None:
		count = result.get('count')+1

		if count != None:
			if config.get("debug") == True:
				print("Message count: " + str(count))

			if count >= config.get("minunread"):
				notify()
				
				for script in config.get("onMessage")["scripts"]:
					enabled = config.get("onMessage")["scripts"][script]
					
					if config.get("debug") == True:
						print(script + " is currently " + conv[enabled])
					
					if(enabled == True):
						exec(open("./res/scripts/" + script + ".py").read())

				time.sleep(60)
			else:
				if config.get("debug") == True:
					print("No new messages.")
				
				time.sleep(25)
		else:
			if config.get("debug") == True:
				print("Ratelimited or not logged in.")

			time.sleep(60)