import requests

from util import cookie

def sendRobloxRequest(URL: str):
    return requests.get(URL,
                        headers={"content-type": "application/json"},
                        cookies={".ROBLOSECURITY": cookie}
                        ).json()
