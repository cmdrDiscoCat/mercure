import discord, config
from discord.ext import commands, tasks

import requests
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup

from config import *
from data import *


# Checks if the user is a server admin
def is_admin():
    def predicate(ctx):
        return ctx.message.author.id in admin_ids
    return commands.check(predicate)


# Checks if we are in the oracle channel, and if we are, that the user who
# wrote the command is in admin
def acces_oracle():
    def verifier_droits_oracle(ctx):
        if str(ctx.message.channel) == 'oracle':
            if ctx.message.author.id in admin_ids:
                return True
            else:
                return False
        else:
            return True
    return commands.check(verifier_droits_oracle)


class Bigbrother(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_bgs.start()
        self.factions_presence = {}

    def cog_unload(self):
        self.daily_bgs.cancel()

    def system_presence_for_faction(self, id_faction):
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
        for id_faction, faction_name in followed_factions.items():
            self.factions_presence[faction_name] = self.system_presence_for_faction(id_faction)

    def bb1984(self, ctx=''):
        """
        Launches a refresh of the systems lists where the factions we follow (set in data.py) are present
        Then, it displays the status of those factions in those systems
        """
        if ctx is None:
            ctx = self.bot.get_channel(config.channel_for_daily_post)

        self.refresh_faction_presence()

        for faction_name,faction_systems in self.factions_presence.items():
            information_block = " "
            if faction_name == "LGC Bulle":
                embed = discord.Embed(title="Bulle", description=information_block, color=0x00ff00)
                url = "http://guilde-cartographes.fr/INFORMATIONS/32MU_STARNEWS/wp-content/uploads/2016/09/LOGO_LGC.png"
            elif faction_name == "LGC Colonia":
                embed = discord.Embed(title="Colonia", description=information_block, color=0x147119)
                url = "http://guilde-cartographes.fr/INFORMATIONS/32MU_STARNEWS/wp-content/uploads/2017/06/colonia.png"
            else:
                embed = discord.Embed(title="{faction}", description=information_block, color=0x147119)
                url = ""
            embed.set_thumbnail(url=url)
            await ctx.send_message(ctx.message.channel, embed=embed)

            information_block = ""
            for faction_system in faction_systems:
                system_quote = urllib.parse.quote(faction_system)
                url_to_call = "https://www.edsm.net/api-system-v1/factions?showHistory=1&systemName=" + system_quote

                try:
                    r = requests.get(url_to_call)
                    informations = r.json()

                    last_update = 0

                    for minor_faction in informations['factions']:
                        if minor_faction['name'] == informations['controllingFaction']['name']:
                            minor_faction_name = "<:lgc:243332108636913665> "
                        else:
                            minor_faction_name = ":black_large_square: "

                        influence_previous = 0

                        if minor_faction['name'] in followed_factions:
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
                except:
                    await ctx.send_message(ctx.message.channel, "Oops ! :crying_cat_face: ")
                    return

                if len(information_block) >= 1000:
                    embed = discord.Embed(description=information_block, color=0x000000)
                    await ctx.send_message(ctx.message.channel, embed=embed)
                    information_block = ""

            # To send the last bit in an embed even if we are under 1000 characters
            if len(information_block) > 0:
                embed = discord.Embed(description=information_block, color=0x000000)
                await ctx.send_message(ctx.message.channel, embed=embed)
                information_block = ""

    @commands.command(pass_context=True)
    @acces_oracle()
    async def bigbrother(self, ctx):
        await self.bb1984(ctx)

    @tasks.loop(minutes=1)
    async def daily_bgs(self):
        if datetime.now().strftime('%H:%M') == '16:00':
            await self.bb1984()
        else:
            pass


def setup(bot):
    bot.add_cog(Bigbrother(bot))
