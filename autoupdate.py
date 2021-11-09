import os
import requests
import shutil

from git.repo.base import Repo

print("Checking for updates...")

online_version_request = requests.get(
    "https://raw.githubusercontent.com/StevenRafft/RobloxMessageNotif/master/version")
online_version = str(online_version_request.content)[2:][:-1]

def move_and_overwrite(root_src_dir: str, root_dst_dir: str):
    # https://stackoverflow.com/questions/7419665/python-move-and-overwrite-files-and-folders#7420617
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                # in case of the src and dst are the same file
                if os.path.samefile(src_file, dst_file):
                    continue
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)


with open(f"./version", "r") as file:
    read = file.read()

    if online_version == read:
        print("No updates found.")
    else:
        print("Found an update!")
        print("Downloading update...")

        if os.path.exists("./.update"):
            if os.path.exists("./.update/.git"):
                os.rename("./.update/.git", "./.update/removeme")
            
            shutil.rmtree("./.update", ignore_errors=True)
            os.rmdir("./.update")
        else:
            os.mkdir("./.update")

        Repo.clone_from(
            "https://github.com/StevenRafft/RobloxMessageNotif", "./.update")

        print("Done downloading!")

        print("Moving extensions and themes...")

        themes = os.listdir("./res/themes/")
        extensions = os.listdir("./res/extensions")

        move_and_overwrite(f"./res/themes", f"./.update/res/themes")
        move_and_overwrite(f"./res/extensions", f"./.update/res/extensions")

        print("Done moving.")
        print("Installing update...")

        move_and_overwrite("./.update", ".")

        print("Done installing!")
        print("Removing temp...")

        shutil.rmtree("./.update", ignore_errors=True)

        print("Done removing temp!")
        print("Update has been successfully installed!")

    print("Current version: %s, Online version: %s" % (read, online_version))
