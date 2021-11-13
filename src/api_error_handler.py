import colorama

colorama.init()

def handle_api_error(result):
    print("%s [ERROR]: Ratelimited or invalid .ROBLOSECURITY key. %s" % (
        colorama.Back.RED, colorama.Style.RESET_ALL))
