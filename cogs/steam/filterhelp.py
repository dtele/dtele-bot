# coding: utf-8

from os import getcwd

import discord
from discord.ext import commands
from reactionmenu import ReactionMenu, Button, ButtonType

from wrapper import Filters


class FilterHelp(commands.Cog):
    def __init__(self, bot, prefix: str) -> None:
        self.bot = bot
        self.prefix = prefix
        self.filters = Filters(f'{getcwd()}/cogs/steam/filters.json')

    @commands.command()
    async def filterhelp(self, ctx, category=''):
        if not category or category not in self.filters.__dict__.keys():
            await ctx.send('```Choose a category out of [tags, types, player_number, supported_os, supported_languages]\n'
                           'Example: +filterhelp tags```')
        else:
            content = list(self.filters.__dict__[category].keys())

            max_len = len(max(content, key=len))
            table = [''.join([j + (' ' * (max_len - len(j))) if x < 4 - 1 else j for x, j in enumerate(content[i:i + 4])]) for i in range(0, len(content), 4)]

            slides = []
            menu = ReactionMenu(ctx, back_button='◀️', next_button='▶️', config=ReactionMenu.STATIC)

            if category == 'tags':
                index = 0
                while index < len(table):
                    count = 0
                    prev_index = index
                    curr_lines = []
                    
                    try:
                        while count < 1800:
                            count += len(table[index])
                            curr_lines.append(table[index])
                            index += 1
                    except IndexError:
                        curr_lines.append(table[prev_index])
                        curr_lines = curr_lines[:-1]

                    slide = discord.Embed(title=f'Valid Arguments for {category}', description='```\n' + '\n'.join(curr_lines) + '```', color=0x1b2838)

                    slides.append(slide)
            else:
                slides = [discord.Embed(title=f'Valid Arguments for {category}', description='```\n' + '\n'.join(content) + '```', color=0x1b2838)]

            for slide in slides:
                slide.set_author(name='', icon_url=ctx.author.avatar_url)
                slide.set_footer(icon_url=r'https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/1200px-Steam_icon_logo.svg.png', text='Data from Steam')
                menu.add_page(slide)

            await menu.start(send_to=ctx.channel)
