from jsonc_parser.parser import JsoncParser

conf = JsoncParser.parse_file("../config.jsonc")
cookie = JsoncParser.parse_file("../cookie.jsonc").get("cookie")

UNREAD_MESSAGES_API_URL = "https://privatemessages.roblox.com/v1/messages/unread/count"
MESSAGES_URL = "https://www.roblox.com/my/messages/#!/inbox"
