import pystray
import ctypes

from os import _exit as exit
from threading import Thread
from PIL import Image

from theme_handler import themeDetails
from util import conf as config
from toggle_window import toggleConsole

trayIcon = None
consoleHiddenState = False

def on_tray_clicked(icon, item):
    trayIcon.stop()

    exit(0)


def toggle_console(icon, item):
    global consoleHiddenState

    toggleConsole()

    consoleHiddenState = not item.checked


def startTrayIcon():
    global trayIcon
    trayIcon = pystray.Icon("Roblox Messsages Notifier", Image.open(themeDetails['msgIcon']), menu=pystray.Menu(
        pystray.MenuItem(
            "Exit",
            on_tray_clicked,
        ),
        pystray.MenuItem(
            "Toggle Console",
            toggle_console,
            checked=lambda item: consoleHiddenState
        )))

    trayIcon.run()


def handleTray():
    if config.get("trayIconEnabled"):
        Thread(target=startTrayIcon).start()

    if config.get("hideWindowOnStart"):
        ctypes.windll.user32.ShowWindow(
            ctypes.windll.kernel32.GetConsoleWindow(), 0)