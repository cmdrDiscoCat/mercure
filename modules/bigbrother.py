import discord, config
from discord.ext import commands, tasks
from main import acces_oracle, is_admin

import requests
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup

from config import *
from data import *


class Bigbrother(commands.Cog):
    def __init__(self, bot):
        if config['DEBUG']: print("Cog Bigbrother initialisé")
        self.bot = bot
        self.ctx = self.bot.get_channel(channel_for_daily_post)
        self.daily_bgs.start()
        self.factions_presence = {}

    def cog_unload(self):
        if config['DEBUG']: print("Cog Bigbrother déchargé")
        self.daily_bgs.cancel()

    def system_presence_for_faction(self, id_faction):
        if config['DEBUG']: print("Fonction system_presence_for_faction")
        r = requests.get("https://inara.cz/galaxy-minorfaction/" + str(id_faction))
        soup = BeautifulSoup(r.text, "html.parser")

        systems = []

        # this works too but it's less elegant
        # systems_links = soup.findAll('a', href=re.compile('^/galaxy-starsystem/'))
        systems_links = soup.select("a[href*='galaxy-starsystem/']")
        for system_link in systems_links:
            systems.append(system_link.get_text())

        # We sort the systems
        systems.sort()

        # Before returning the list, we remove duplicates by..
        # converting back a dict containing the unique keys of our list... into a list
        return list(dict.fromkeys(systems))

    def refresh_faction_presence(self):
        if config['DEBUG']: print("Fonction refresh_faction_presence")
        for id_faction, faction_name in followed_factions.items():
            self.factions_presence[faction_name] = self.system_presence_for_faction(id_faction)

    async def bb1984(self, ctx=''):
        """
        Launches a refresh of the systems lists where the factions we follow (set in data.py) are present
        Then, it displays the status of those factions in those systems
        """
        if config['DEBUG']: print("Commande bb1984")
        if ctx is None:
            ctx = self.ctx

        print(ctx)
        self.refresh_faction_presence()

        for faction_name, faction_systems in self.factions_presence.items():
            information_block = " "
            if faction_name == "LGC - Cartographers's Guild":
                embed = discord.Embed(title="Bulle", description=information_block, color=0x00ff00)
                url = "http://guilde-cartographes.fr/INFORMATIONS/32MU_STARNEWS/wp-content/uploads/2016/09/LOGO_LGC.png"
            elif faction_name == "LGC - Colonia Cartographers' Guild":
                embed = discord.Embed(title="Colonia", description=information_block, color=0x147119)
                url = "http://guilde-cartographes.fr/INFORMATIONS/32MU_STARNEWS/wp-content/uploads/2017/06/colonia.png"
            else:
                embed = discord.Embed(title="{faction_name}", description=information_block, color=0x147119)
                url = ""
            embed.set_thumbnail(url=url)
            await ctx.send(embed=embed)

            information_block = ""
            for faction_system in faction_systems:
                print("BB1984 for "+faction_system)
                system_quote = urllib.parse.quote(faction_system)
                url_to_call = "https://www.edsm.net/api-system-v1/factions?showHistory=1&systemName=" + system_quote

                r = requests.get(url_to_call)
                informations = r.json()

                last_update = 0

                for minor_faction in informations['factions']:
                    print("BB1984 parcours des factions de " + faction_system+ " pour recherche de la nôtre")
                    if minor_faction['name'] == informations['controllingFaction']['name']:
                        minor_faction_name = "<:lgc:243332108636913665> "
                    else:
                        minor_faction_name = ":black_large_square: "

                    influence_previous = 0

                    print(minor_faction['name'])
                    print(followed_factions.values())

                    if minor_faction['name'] in followed_factions.values():
                        print("BB1984 on est là !")
                        if minor_faction['lastUpdate'] > last_update:
                            last_update = minor_faction['lastUpdate']

                        last_update = datetime.fromtimestamp(last_update)
                        information_block += minor_faction_name + informations['name']

                        if minor_faction['influenceHistory']:
                            for date, history in minor_faction['influenceHistory'].items():
                                if (history != minor_faction['influence']
                                        and int(date) < int(minor_faction['lastUpdate'])):
                                    influence_previous = history
                            information_block += " *[{0:.2f}".format(float(100 * float(influence_previous)))
                            information_block +=  "%]* > "

                        information_block += "**[{:.2%}".format(minor_faction['influence']) + "]**"
                        information_block += " | " + traduction[minor_faction['state']]
                        information_block += " *(" + last_update.strftime("%d/%m-%Hh%M") + ")*\n"

                if len(information_block) >= 1000:
                    embed = discord.Embed(description=information_block, color=0x000000)
                    await ctx.send(embed=embed)
                    information_block = ""

            # To send the last bit in an embed even if we are under 1000 characters
            if len(information_block) > 0:
                embed = discord.Embed(description=information_block, color=0x000000)
                await ctx.send(embed=embed)
                information_block = ""

    @commands.command(pass_context=True)
    @acces_oracle()
    async def bigbrother(self, ctx):
        if config['DEBUG']: print("Commande bigbrother")
        await self.bb1984(ctx)

    @tasks.loop(minutes=1)
    async def daily_bgs(self):
        if config['DEBUG']: print("Loop daily_bgs")
        if datetime.now().strftime('%H:%M') == '16:30':
            await self.bb1984()
        else:
            pass


def setup(bot):
    bot.add_cog(Bigbrother(bot))
