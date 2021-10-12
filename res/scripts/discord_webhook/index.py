# This script was made by jackssrt (https://github.com/jackssrt)

from discord import Webhook, RequestsWebhookAdapter, embeds
from jsonc_parser.parser import JsoncParser

import discord

WEBHOOK_URL = JsoncParser.parse_file(
    "./res/scripts/discord_webhook/precious_info.jsonc").get("token")

embed = discord.embeds.Embed()
embed.title = "new message"
embed.description = "steve got new message on roblos"
webhook = Webhook.from_url(
    WEBHOOK_URL, adapter=RequestsWebhookAdapter())
webhook.send(embed=embed)
