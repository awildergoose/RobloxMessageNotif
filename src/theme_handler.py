import colorama

from jsonc_parser.parser import JsoncParser
from util import conf as config

colorama.init()

theme = config.get("onMessage")["theme"]
themeFile = JsoncParser.parse_file(f"../res/themes/{theme}.jsonc")
themeDetails = {
    "msgTitle": themeFile.get("title"),
    "msgContent": themeFile.get("content"),
    "msgDuration": themeFile.get("duration")
}

def handle():
    try:
        themeDetails["msgIcon"] = f"../res/icons/{themeFile.get('icon')}.ico"
    except:
        # i dont think this works, someone please make a pull request if u can fix this
        print("%s [WARNING]: Icon not provided for theme %s using default theme. (../res/icons/default.ico) %s" %
            (colorama.Back.LIGHTBLACK_EX, theme, colorama.Style.RESET_ALL))

        themeDetails["msgIcon"] = "../res/icons/default.ico"