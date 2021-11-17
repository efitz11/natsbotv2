# bot.py
from discord import Intents
from discord.ext.commands import Bot
from discord_slash import SlashCommand
import utils

# Note that command_prefix is a required but essentially unused paramater.
# Setting help_command=False ensures that discord.py does not create a !help command.
# Enabling self_bot ensures that the bot does not try and parse messages that start with "!".

bot = Bot(command_prefix="&", self_bot=True, help_command=None, intents=Intents.default())
slash = SlashCommand(bot, sync_commands=True)


bot.load_extension("baseball")
discord_token = utils.get_keys('discord')['bot_token']

bot.run(discord_token)
