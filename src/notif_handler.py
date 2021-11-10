import webbrowser

from win10toast_click import ToastNotifier
from theme_handler import themeDetails
from util import MESSAGES_URL

def _on_click():
    webbrowser.open_new(MESSAGES_URL)

def notify():
    toast = ToastNotifier()
    toast.show_toast(themeDetails["msgTitle"], themeDetails["msgContent"], duration=themeDetails["msgDuration"],
                     icon_path=themeDetails["msgIcon"], threaded=True, callback_on_click=_on_click)
