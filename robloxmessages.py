import colorama
import webbrowser
import requests
import time

from jsonc_parser.parser import JsoncParser
from win10toast_click import ToastNotifier

cookie = JsoncParser.parse_file("./cookie.jsonc").get("cookie")
config = JsoncParser.parse_file("./config.jsonc")

theme = config.get("onMessage")["theme"]
themeFile = JsoncParser.parse_file("./res/themes/%s.jsonc" % theme)
themeDetails = {
    "msgTitle": themeFile.get("title"),
    "msgContent": themeFile.get("content"),
    "msgDuration": themeFile.get("duration")
}

colorama.init()

try:
    themeDetails["msgIcon"] = "./res/icons/%s.ico" % themeFile.get("icon")
except:
    # i don't think this works, someone please make a pull request if u can fix this
    print("%s [WARNING]: Icon not provided for theme %s using default theme. (./res/icons/default.ico) %s" %
          (colorama.Back.LIGHTBLACK_EX, theme, colorama.Style.RESET_ALL))

    themeDetails["msgIcon"] = "./res/icons/default.ico"

API_URL = "https://privatemessages.roblox.com/v1/messages/unread/count"
PAGE_URL = "https://www.roblox.com/my/messages/#!/inbox"

def onClick():
    webbrowser.open_new(PAGE_URL)

def notify():
    toast = ToastNotifier()
    toast.show_toast(themeDetails["msgTitle"], themeDetails["msgContent"], duration=themeDetails["msgDuration"],
                     icon_path=themeDetails["msgIcon"], threaded=True, callback_on_click=onClick)

def sendRobloxRequest(URL):
    return requests.get(API_URL,
                            headers={"content-type": "application/json"},
                            cookies={".ROBLOSECURITY": cookie}
                            ).json()


while True:
    result = sendRobloxRequest(API_URL)
    if result == None:
        continue

    count = result.get("count")
    if count == None:
        if config.get("debug"):
            print("%s [ERROR]: Ratelimited or invalid .ROBLOSECURITY key. %s" % (
                colorama.Back.RED, colorama.Style.RESET_ALL))

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
