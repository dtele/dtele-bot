# coding: utf-8

from copy import deepcopy
from os import getcwd

import discord
from discord.ext import commands
from reactionmenu import ButtonsMenu, ComponentsButton

from wrapper import App, Bundle, Filters, Search


class Steam(commands.Cog):
    def __init__(self, bot, prefix: str) -> None:
        self.bot = bot
        self.prefix = prefix
        self.filters = Filters(f'{getcwd()}/cogs/steam/filters.json')
        self.sm = Search()

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message) -> None:
        ctx = await self.bot.get_context(msg)

        if msg.content == self.prefix + 'help steam':
            await ctx.send('```\nArguments: region (positional, unspaced), search_term (positional)\n'
                           'Example: +steamin stellaris```')

        elif msg.content == self.prefix + 'help fsteam':
            await ctx.send('```\nArguments: region (positional, unspaced), search_term, discounted, tags, types, player_number, supported_os, supported_languages\n'
                           'Example: +fsteamar search_term=stellaris;tags=[4x, space];supported_os=[windows, mac os x]```')

        elif msg.content.startswith(self.prefix + 'steam'):
            cc = msg.content.split(' ')[0][6:]
            term = ' '.join(msg.content.split(' ')[1:])

            result = self.sm.search(search_term=term)

            try:
                await Steam.output(ctx=ctx, app=[i for i in result if isinstance(i, App)][0], cc=cc).start()
            except IndexError:
                await ctx.send(embed=discord.Embed(title=':warning: An Error Occurred', description='error notes: no apps found with matching name', color=0x1b2838))

        elif msg.content.startswith(self.prefix + 'fsteam'):
            cc = msg.content.split(' ')[0][7:]
            search_filters = msg.content[msg.content.find(' ') + 1:].split(';')
            kwargs = {'search_term': '', 'discounted': False, 'tags': '', 'types': '', 'player_number': '', 'supported_os': '', 'supported_languages': ''}

            for i in search_filters:
                k, v = i.split('=')
                # turn raw str to list
                if v[0] == '[' and v[-1] == ']':
                    v = [i.strip(' ') for i in v[1:-1].split(',')]
                # translate text to steam filter codes
                if k in self.filters.__dict__.keys():
                    if isinstance(v, list):
                        v = [self.filters.__dict__[k][i] for i in v]
                    else:
                        v = self.filters.__dict__[k][v]

                kwargs[k] = v

            result = self.sm.advanced_search(search_term=kwargs["search_term"], discounted=kwargs["discounted"],
                                             tags=kwargs["tags"], types=kwargs["types"], player_number=kwargs["player_number"],
                                             supported_os=kwargs["supported_os"], supported_languages=kwargs["supported_languages"])

            try:
                await Steam.output(ctx=ctx, app=[i for i in result if isinstance(i, App)][0], cc=cc).start()
            except IndexError:
                await ctx.send(embed=discord.Embed(title=':warning: An Error Occurred', description='error notes: no apps found with matching name', color=0x1b2838))

    @staticmethod
    def output(ctx, app: App, cc: str) -> ButtonsMenu:
        details = app.details(cc=cc)

        try:
            sys_requirements = details["pc_requirements"]["minimum"]
            sys_requirements_embed = discord.Embed(title='Minimum System Requirements', color=0x1b2838)
            for i in [f'{i}:</strong>' for i in ['OS', 'Processor', 'Memory', 'Graphics']]:
                try:
                    temp = sys_requirements[sys_requirements.index(i) + len(i):]
                    sys_requirements_embed.add_field(name=i[:i.index(':')], value=temp[:temp.index('<br>')].replace('&amp;', '&'), inline=False)
                except ValueError:
                    continue
        except (IndexError, KeyError) as e:
            sys_requirements_embed = discord.Embed(title=':warning: An Error Occurred', description='notes: system requirements parsing failed, probably due to non-standard formatting', color=0x1b2838)

        if details["is_free"]:
            price = "Free"
        else:
            try:
                price = dict(details["price_overview"])
                if price["initial_formatted"]:
                    price = f'~~{price["initial_formatted"]}~~ {price["final_formatted"]} (-{price["discount_percent"]}%)'
                else:
                    price = price["final_formatted"]
            except KeyError:
                price = 'Not Available'

        menu = ButtonsMenu(ctx, menu_type=ButtonsMenu.TypeEmbed, timeout=300)

        info_page = discord.Embed(title=details["name"], url=rf'https://store.steampowered.com/app/{details["steam_appid"]}', description=details["short_description"], color=0x1b2838)

        info_page.set_image(url=details["header_image"])
        info_page.set_author(name=', '.join(details["developers"]) if 'developers' in details.keys() else ', '.join(details["publishers"]), url=details["website"] if details["website"] else 'https://store.steampowered.com/', icon_url=ctx.author.avatar_url)
        info_page.set_footer(icon_url=r'https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/1200px-Steam_icon_logo.svg.png', text='Data from Steam')
        info_page.add_field(name='Release Date', value=f'Soon ({details["release_date"]["date"]})' if details["release_date"]["coming_soon"] else details["release_date"]["date"], inline=True)
        info_page.add_field(name='Genres', value=', '.join([i["description"] for i in details["genres"]]), inline=True)
        info_page.add_field(name='Price', value=price, inline=True)
        info_page.add_field(name='Metacritic Score', value=details["metacritic"]["score"] if 'metacritic' in details.keys() else 'Not Available', inline=True)
        info_page.add_field(name='Operating Systems', value=' '.join([i[0] for i in list(zip(['<:windows:849801121567735808>', '<:mac:849800699721416735>', '<:linux:849800846177992704>'], [i for i in details["platforms"].values()])) if i[1]]), inline=True)
        info_page.add_field(name='Multiplayer', value='Yes' if 'multiplayer' in ''.join([i["description"].lower().replace('-', '') for i in details["categories"]]).replace(' ', '') else 'No', inline=True)

        menu.add_page(info_page)

        for screenshot in details["screenshots"]:
            temp_page = deepcopy(info_page)
            temp_page.set_image(url=screenshot["path_full"])

            menu.add_page(temp_page)

        menu.add_button(ComponentsButton(style=ComponentsButton.style.primary, label='Back', custom_id=ComponentsButton.ID_PREVIOUS_PAGE))
        menu.add_button(ComponentsButton(style=ComponentsButton.style.primary, label='Next', custom_id=ComponentsButton.ID_NEXT_PAGE))
        menu.add_button(ComponentsButton(style=ComponentsButton.style.secondary, label='System Requirements', custom_id=ComponentsButton.ID_SEND_MESSAGE, followup=ComponentsButton.Followup(embed=sys_requirements_embed)))

        return menu
