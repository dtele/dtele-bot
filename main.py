import json
import sys
from os import getcwd, listdir
from random import randrange
from re import sub

import discord
from discord.ext import commands
from reactionmenu import ButtonsMenu, ComponentsButton

cogs_to_path = [sys.path.append(rf'{getcwd()}\cogs\{i}') for i in listdir(rf'{getcwd()}\cogs')]

from filterhelp import FilterHelp
from m_steam import Steam
from webster import Dictionary
from tmdb import Tmdb


with open('preferences.json', 'r') as file:
    keys = json.load(file)

prefix = keys["prefix"]
bot = commands.Bot(command_prefix=prefix)
ButtonsMenu.initialize(bot=bot)

bot.add_cog(Steam(bot, prefix))
bot.add_cog(FilterHelp(bot, prefix))
bot.add_cog(Dictionary(bot, prefix, keys["webster_key"]))
bot.add_cog(Tmdb(bot, prefix, keys["tmdb_key"]))

bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'{bot.user.name} online\nServers: {", ".join([i.name for i in list(bot.guilds)])}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=keys["activity"]))


@bot.event
async def on_message(msg):
    ctx = await bot.get_context(msg)
    text = sub('https?:\/\/\S+\.\w+\/\S+\/\S+', '', msg.content)
    if not msg.author.bot:
        if 'bruh' in text:
            await ctx.send('bruh')
        elif '69' in text:
            await ctx.send(
                f'{":rofl:" * randrange(1, 4 + 1)} {"lo" * randrange(3, 8 + 1) + "l"} 69 {":thumbsup:" * randrange(1, 4 + 1)}')

    await bot.process_commands(msg)


bot.run(keys["discord_key"])
