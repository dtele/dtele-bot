# coding: utf-8

import json
import sys
from os import getcwd, listdir

import discord
from discord.ext import commands
from reactionmenu import ButtonsMenu, ComponentsButton

cogs_to_path = [sys.path.append(rf'{getcwd()}\cogs\{i}') for i in listdir(rf'{getcwd()}\cogs')]

from filterhelp import FilterHelp
from m_steam import Steam
from webster import Dictionary


with open('preferences.json', 'r') as file:
    keys = json.load(file)

prefix = keys["prefix"]
bot = commands.Bot(command_prefix=prefix)
ButtonsMenu.initialize(bot=bot)

bot.add_cog(Steam(bot, prefix))
bot.add_cog(FilterHelp(bot, prefix))
bot.add_cog(Dictionary(bot, prefix, keys["webster_key"]))

bot.remove_command('help')


@bot.event
async def on_message(msg):
    ctx = await bot.get_context(msg)
    if 'bruh' in msg.content and not msg.author.bot:
        await ctx.send('bruh')

    await bot.process_commands(msg)


@bot.event
async def on_ready():
    print(f'{bot.user.name} online\nServers: {", ".join([i.name for i in list(bot.guilds)])}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=keys["activity"]))


bot.run(keys["discord_key"])
