import requests

import discord
from discord.ext import commands


class Dictionary(commands.Cog):
    def __init__(self, bot, prefix: str, thesaurus_key: str):
        self.bot = bot
        self.prefix = prefix
        self.key = thesaurus_key

    @commands.command()
    async def meaning(self, ctx, word):
        link = f'https://dictionaryapi.com/api/v3/references/ithesaurus/json/{word}?key={self.key}'
        data = requests.get(link).json()[0]
        try:
            meaning_embed = discord.Embed(title=f'{word} ({data["fl"]})', url=f'https://www.merriam-webster.com/dictionary/{word}', color=0x004990)
            meaning_embed.set_footer(icon_url=r'https://www.dictionaryapi.com/images/info/branding-guidelines/MWLogo_LightBG_120x120_2x.png', text='Data from Merriam-Webster')
            meaning_embed.add_field(name='Meaning', value='\n'.join(['• ' + i for i in data["shortdef"]]), inline=True)
            meaning_embed.add_field(name='Synonyms', value=', '.join([i[0] for i in data["meta"]["syns"]]), inline=True)

            await ctx.send(embed=meaning_embed)
        except (KeyError, TypeError):
            await ctx.send(embed=discord.Embed(title=':warning: An Error Occurred', description='notes: only works for correctly spelled words', color=0x1b2838))
