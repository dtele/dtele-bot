import requests
from requests.utils import requote_uri

import discord
from discord.ext import commands


class Tmdb(commands.Cog):
    def __init__(self, bot, prefix: str, tmdb_key: str):
        self.sesh = requests.Session()
        self.bot = bot
        self.prefix = prefix
        self.key = tmdb_key

    @commands.command()
    async def tmdb(self, ctx, *user_text: str):
        user_text = ' '.join(user_text)
        args = user_text.split(':')
        year = args[-1] if len(args) > 1 else None
        term = args[0]

        search_result = self.sesh.get(f'https://api.themoviedb.org/3/search/movie?api_key={self.key}&query={requote_uri(term)}&include_adult=false{"&year=" + year if year else ""}').json()["results"]
        if len(search_result) > 0:
            movie = self.sesh.get(f'https://api.themoviedb.org/3/movie/{search_result[0]["id"]}?api_key={self.key}').json()

            movie_embed = discord.Embed(title=f'{movie["title"]} ({movie["release_date"].split("-")[0]})', url=f'https://www.themoviedb.org/movie/{movie["id"]}', description=movie["overview"], color=0x90cea1)
            movie_embed.set_thumbnail(url=f'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/{movie["poster_path"][1:]}')
            movie_embed.set_footer(icon_url='https://themoviedb.org/assets/2/v4/icons/mstile-144x144-30e7905a8315a080978ad6aeb71c69222b72c2f75d26dab1224173a96fecc962.png', text='Data from TMDb')
            movie_embed.add_field(name='Genre(s)', value=', '.join([i["name"] for i in movie["genres"]]) if movie["genres"] else 'Not Available', inline=True)
            movie_embed.add_field(name='Runtime', value=f'{movie["runtime"] // 60}h {movie["runtime"] % 60}m' if movie["runtime"] else 'Not Available', inline=True)
            movie_embed.add_field(name='Rating', value=f'{movie["vote_average"]} ({"{:,}".format(int(movie["vote_count"]))} votes)' if movie["vote_count"] else 'Not Available', inline=True)
            movie_embed.add_field(name='Language(s)', value= (', '.join([i["english_name"] for i in movie["spoken_languages"]])) if movie["spoken_languages"] else 'Not Available', inline=True)

            await ctx.send(embed=movie_embed)
        else:
            await ctx.send(embed=discord.Embed(title=':warning: An Error Occurred', description='error notes: no movies found with matching name', color=0x01d473))
