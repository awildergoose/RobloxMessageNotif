import requests
import time

import win10toast
from jsonc_parser.parser import JsoncParser

cookie = JsoncParser.parse_file('./conf.jsonc').get("cookie")

url = "https://privatemessages.roblox.com/v1/messages/unread/count"
cookies = {'.ROBLOSECURITY': cookie}

def notify():
    toast = win10toast.ToastNotifier()
    toast.show_toast("Message", "You got a new message!", duration=3, icon_path="./icon.ico", threaded=True, sound=False)

while True:
	urlHandler = requests.get(url, headers={"content-type": "application/json"}, cookies=cookies)
	result = urlHandler.json()
	
	if result != None:
		count = result.get('count')

		if count != None:
			if count >= 1:
				notify()
				time.sleep(60)
			else:
				time.sleep(25)
		else:
			print("Ratelimited or not logged in.")
			time.sleep(60)