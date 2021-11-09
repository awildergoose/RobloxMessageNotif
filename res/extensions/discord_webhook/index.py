# This script was made by jackssrt (https://github.com/jackssrt)

from discord import Webhook, RequestsWebhookAdapter, embeds
from jsonc_parser.parser import JsoncParser

WEBHOOK_URL: str = JsoncParser.parse_file(
    "./res/extensions/discord_webhook/precious_info.jsonc").get("token")

embed = embeds.Embed()
embed.title = "new message"
embed.description = "steve got new message on roblos"
webhook = Webhook.from_url(
    WEBHOOK_URL, adapter=RequestsWebhookAdapter())
webhook.send(embed=embed)