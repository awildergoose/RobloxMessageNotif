import requests
import time

import win10toast
from jsonc_parser.parser import JsoncParser

cookie = JsoncParser.parse_file('./cookie.jsonc').get("cookie")
config = JsoncParser.parse_file('./config.jsonc')

API_URL = "https://privatemessages.roblox.com/v1/messages/unread/count"

def notify():
    toast = win10toast.ToastNotifier()
    toast.show_toast("Message", "You got a new message!", duration=10, icon_path="./icon.ico", threaded=True, sound=False)

while True:
	urlHandler = requests.get(API_URL,
	    headers = {"content-type": "application/json"},
	    cookies = {'.ROBLOSECURITY': cookie}
	)

	result = urlHandler.json()
	
	if result != None:
		count = result.get('count')

		if count != None:
			if count >= config.get("minunread"):
				notify()
				time.sleep(60)
			else:
				time.sleep(25)
		else:
			print("Ratelimited or not logged in.")
			time.sleep(60)