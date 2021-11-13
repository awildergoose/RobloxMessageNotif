# #############################################
# ############## TO DO ########################
# #############################################
# Error Notifications (toggle)
# Enable colorama colors (toggle)
# Marketplace (currently being worked on)
# #############################################
# #############################################
# #############################################

# #################################################
# ############## Bug Fixes ########################
# #################################################
# Fix AutoUpdate's file deletion error that gets called because of the hidden .git folder
# > Use the os.system function to delete the folder using something like
# >>    os.system("del ../.update")
# #################################################
# #################################################
# #################################################

import time

from auto_update import check as checkForUpdates
from api_handler import sendRobloxRequest
from api_error_handler import handle_api_error
from tray_handler import handleTray as handle_tray
from notif_handler import notify
from extension_handler import handle as handle_extensions
from theme_handler import handle as handle_theme
from util import conf as config
from util import UNREAD_MESSAGES_API_URL

if config.get("autoUpdate"):
    checkForUpdates()

handle_theme()
handle_tray()

while True:
    result = sendRobloxRequest(UNREAD_MESSAGES_API_URL)
    if result == None:
        continue

    count = result.get("count")
    if count == None:
        if config.get("debug"):
            handle_api_error(result)
        
        time.sleep(60)
        continue

    if config.get("debug"):
        print(f"Message count: {str(count)}")

    if count >= config.get("minunread"):
        notify()

        handle_extensions()

        time.sleep(60)
    else:
        if config.get("debug"):
            print("No new messages.")

        time.sleep(25)
