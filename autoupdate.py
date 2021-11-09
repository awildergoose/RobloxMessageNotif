import os
import requests
import shutil

from git.repo.base import Repo

print("Checking for updates...")

online_version_request = requests.get("https://raw.githubusercontent.com/StevenRafft/RobloxMessageNotif/master/version")
online_version = str(online_version_request.content)[2:][:-1]

with open(f"./version", "r") as file:
    read = file.read()

    if online_version == read:
        print("No updates found.")
    else:
        print("Found an update!")
        print("Downloading update...")

        if os.path.exists("./.update"):
            shutil.rmtree("./.update")
        
        os.mkdir("./.update")

        Repo.clone_from("https://github.com/StevenRafft/RobloxMessageNotif", "./.update")

        print("Done downloading!")

        print("Moving extensions and themes...")

        themes = os.listdir("./res/themes/")
        extensions = os.listdir("./res/extensions")

        for theme in themes:
            print("Moved %s to %s" % (("./res/themes/%s" % theme), ("./.update/res/themes/%s" % theme)))
            os.replace("./res/themes/%s" % theme, "./.update/res/themes/%s" % theme)
        
        for extension in extensions:
            print("Moved %s to %s" % (("./res/extensions/%s" % extension), ("./.update/res/extensions/%s" % extension)))
            shutil.move("./res/extensions/%s" % extension, "./.update/res/extensions/%s" % extension)
        
        print("Done moving.")
        print("Installing update...")

        shutil.copy("./.update", "./")

        print("Done installing!")

        print("Removing temp...")

        shutil.rmtree("./.update")

        print("Done removing temp!")

        print("Update has been successfully installed!")
    

    print("Current version: %s, Online version: %s" % (read, online_version))