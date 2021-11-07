import colorama
import win10toast
import requests
import time

from jsonc_parser.parser import JsoncParser

cookie = JsoncParser.parse_file("./cookie.jsonc").get("cookie")
config = JsoncParser.parse_file("./config.jsonc")

theme = config.get("onMessage")["theme"]
themeFile = JsoncParser.parse_file("./res/themes/%s.jsonc" % theme)
themeDetails = {
    "msgTitle": themeFile.get("title"),
    "msgContent": themeFile.get("content"),
    "msgDuration": themeFile.get("duration"),
    "icon": ""
}

colorama.init()

try:
    themeDetails["icon"] = "./res/icons/%s.ico" % themeFile.get("icon")
except TypeError:
    print("%s [WARNING]: Icon not provided for theme %s using default theme. (./res/icons/default.ico) %s" % (colorama.Back.LIGHTBLACK_EX, theme, colorama.Style.RESET_ALL))

    themeDetails["icon"] = "./res/icons/default.ico"

API_URL = "https://privatemessages.roblox.com/v1/messages/unread/count"


def notify():
    toast = win10toast.ToastNotifier()
    toast.show_toast(themeDetails.msgTitle, themeDetails.msgContent, duration=themeDetails.msgDuration,
                     icon_path=themeDetails.icon, threaded=True, sound=False)


while True:
    result = requests.get(API_URL,
                          headers={"content-type": "application/json"},
                          cookies={".ROBLOSECURITY": cookie}
                          ).json()
    if result == None:
        continue

    count = result.get("count")
    if count == None:
        if config.get("debug"):
            print("%s [ERROR]: Ratelimited or invalid .ROBLOSECURITY key. %s" % (colorama.Back.RED, colorama.Style.RESET_ALL))

        time.sleep(60)
        continue

    if config.get("debug"):
        print("Message count: %s" % str(count))

    if count >= config.get("minunread"):
        notify()

        for script in config.get("onMessage")["scripts"]:
            enabled = config.get("onMessage")["scripts"][script]

            if config.get("debug"):
                print(
                    f"{script} is currently {'enabled' if enabled else 'disabled'}")

            if enabled:
                with open(f"./res/scripts/{script}/index.py") as file:
                    exec(file.read())

        time.sleep(60)
    else:
        if config.get("debug"):
            print("No new messages.")

        time.sleep(25)
