from util import conf as config

def handle():
    for extension in config.get("onMessage")["extensions"]:
            enabled = config.get("onMessage")["extensions"][extension]

            if config.get("debug"):
                print(
                    f"{extension} is currently {'enabled' if enabled else 'disabled'}")

            if enabled:
                with open(f"../res/extensions/{extension}/index.py") as file:
                    exec(file.read())