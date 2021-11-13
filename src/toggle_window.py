import ctypes

consoleHidden = False

def toggleConsole():
    global consoleHidden

    if(consoleHidden):
        ctypes.windll.user32.ShowWindow(
            ctypes.windll.kernel32.GetConsoleWindow(), 1)
    else:
        ctypes.windll.user32.ShowWindow(
            ctypes.windll.kernel32.GetConsoleWindow(), 0)

    consoleHidden = not consoleHidden