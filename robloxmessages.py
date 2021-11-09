import ctypes
import pystray
import colorama
import webbrowser
import requests
import time

from os import _exit as exit
from os import getppid as getppid
from threading import Thread
from jsonc_parser.parser import JsoncParser
from win10toast_click import ToastNotifier
from PIL import Image

config = JsoncParser.parse_file("./config.jsonc")

if config.get("autoUpdate"):
    with open(f"./autoupdate.py") as file:
        exec(file.read())

cookie = JsoncParser.parse_file("./cookie.jsonc").get("cookie")

consoleHidden = False
consoleHiddenState = False

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

trayIcon = None


def on_tray_clicked(icon, item):
    trayIcon.stop()

    exit(0)


def toggle_console(icon, item):
    global consoleHiddenState
    global consoleHidden

    if(consoleHidden):
        ctypes.windll.user32.ShowWindow(
            ctypes.windll.kernel32.GetConsoleWindow(), 1)
    else:
        ctypes.windll.user32.ShowWindow(
            ctypes.windll.kernel32.GetConsoleWindow(), 0)

    consoleHidden = not consoleHidden
    consoleHiddenState = not item.checked


def startTrayIcon():
    global trayIcon
    trayIcon = pystray.Icon('Roblox Messsages Notifier', Image.open('./res/icons/default.ico'), menu=pystray.Menu(
        pystray.MenuItem(
            'Exit',
            on_tray_clicked,
        ),
        pystray.MenuItem(
            'Toggle Console',
            toggle_console,
            checked=lambda item: consoleHiddenState
        )))

    trayIcon.run()


if config.get("trayIconEnabled"):
    Thread(target=startTrayIcon).start()

if config.get("hideWindow"):
    ctypes.windll.user32.ShowWindow(
        ctypes.windll.kernel32.GetConsoleWindow(), 0)

consoleHidden = True


def onClick():
    webbrowser.open_new(PAGE_URL)


def notify():
    toast = ToastNotifier()
    toast.show_toast(themeDetails["msgTitle"], themeDetails["msgContent"], duration=themeDetails["msgDuration"],
                     icon_path=themeDetails["msgIcon"], threaded=True, callback_on_click=onClick)


def sendRobloxRequest(URL: str):
    return requests.get(URL,
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

        for extension in config.get("onMessage")["extensions"]:
            enabled = config.get("onMessage")["extensions"][extension]

            if config.get("debug"):
                print(
                    f"{extension} is currently {'enabled' if enabled else 'disabled'}")

            if enabled:
                with open(f"./res/extensions/{extension}/index.py") as file:
                    exec(file.read())

        time.sleep(60)
    else:
        if config.get("debug"):
            print("No new messages.")

        time.sleep(25)
