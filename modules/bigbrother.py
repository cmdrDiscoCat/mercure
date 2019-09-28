import discord, config
from discord.ext import commands, tasks

import requests
import urllib.parse
from datetime import datetime

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

    def cog_unload(self):
        self.daily_bgs.cancel()

    async def bb1984(self, ctx=''):
        """
        Like the above, but instead of links, the information is displayed
        """
        if ctx == None:
            ctx = self.bot.get_channel(config.channel_for_daily_post)

        bloc_information = " "
        embed = discord.Embed(title="Bulle", description=bloc_information, color=0x00ff00)
        url = "http://guilde-cartographes.fr/INFORMATIONS/32MU_STARNEWS/wp-content/uploads/2016/09/LOGO_LGC.png"
        embed.set_thumbnail(url=url)
        await ctx.send_message(ctx.message.channel, embed=embed)

        bloc_information = ""
        for nom_systeme, systeme in systemes_bulle.items():
            nom_systeme_quote = urllib.parse.quote(nom_systeme)
            url_to_call = "https://www.edsm.net/api-system-v1/factions?showHistory=1&systemName=" + nom_systeme_quote

            try:
                r = requests.get(url_to_call)
                informations = r.json()

                last_update = 0

                for faction in informations['factions']:
                    if faction['name'] == informations['controllingFaction']['name']:
                        nom_faction = "<:lgc:243332108636913665> "
                    else:
                        nom_faction = ":black_large_square: "

                    influencePrevious = 0

                    if faction['name'] in nom_factions:

                        if (faction['lastUpdate'] > last_update):
                            last_update = faction['lastUpdate']
                        last_update = datetime.fromtimestamp(last_update)
                        bloc_information += nom_faction + informations['name']
                        if faction['influenceHistory']:
                            for date, history in faction['influenceHistory'].items():
                                if history != faction['influence'] and int(date) < int(faction['lastUpdate']):
                                    influencePrevious = history
                            bloc_information += " *[{0:.2f}".format(float(100 * float(influencePrevious))) + "%]* > "
                        bloc_information += "**[{:.2%}".format(faction['influence']) + "]**"
                        bloc_information += " | " + traduction[faction['state']]
                        bloc_information += " *(" + last_update.strftime("%d/%m-%Hh%M") + ")*\n"
            except:
                await ctx.send_message(ctx.message.channel, "Oops, problème droit devant ! :crying_cat_face: ")
                return

            if len(bloc_information) >= 1000:
                embed = discord.Embed(description=bloc_information, color=0x000000)
                await ctx.send_message(ctx.message.channel, embed=embed)
                bloc_information = ""

        # To send the last bit in an embed even if we are under 1000 characters
        if len(bloc_information) > 0:
            embed = discord.Embed(description=bloc_information, color=0x000000)
            await ctx.send_message(ctx.message.channel, embed=embed)
            bloc_information = ""

        bloc_information = " "
        embed = discord.Embed(title="Colonia", description=bloc_information, color=0x147119)
        url = "http://guilde-cartographes.fr/INFORMATIONS/32MU_STARNEWS/wp-content/uploads/2017/06/colonia.png"
        embed.set_thumbnail(url=url)
        await ctx.send_message(ctx.message.channel, embed=embed)

        bloc_information = ""
        for nom_systeme, systeme in systemes_colonia.items():

            nom_systeme_quote = urllib.parse.quote(nom_systeme)
            url_to_call = "https://www.edsm.net/api-system-v1/factions?showHistory=1&systemName=" + nom_systeme_quote

            try:
                r = requests.get(url_to_call)
                informations = r.json()

                last_update = 0

                for faction in informations['factions']:
                    if faction['name'] == informations['controllingFaction']['name']:
                        nom_faction = "<:lgc:243332108636913665> "
                    else:
                        nom_faction = ":black_large_square: "

                    influencePrevious = 0

                    if faction['name'] in nom_factions:
                        if (faction['lastUpdate'] > last_update):
                            last_update = faction['lastUpdate']
                        last_update = datetime.fromtimestamp(last_update)
                        bloc_information += nom_faction + informations['name']
                        for date, history in faction['influenceHistory'].items():
                            if history != faction['influence'] and int(date) < int(faction['lastUpdate']):
                                influencePrevious = history
                        bloc_information += " *[{:.2%}".format(influencePrevious) + "]* > "
                        bloc_information += "**[{:.2%}".format(faction['influence']) + "]**"
                        bloc_information += " | " + traduction[faction['state']]
                        bloc_information += " *(" + last_update.strftime("%d/%m-%Hh%M") + ")*\n"
            except:
                await ctx.send_message(ctx.message.channel, "Oops, problème droit devant ! :crying_cat_face: ")
                return

        embed = discord.Embed(description=bloc_information, color=0x000000)
        await ctx.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True)
    @acces_oracle()
    async def bigbrother(self, ctx):
        await self.bb1984()

    @tasks.loop(minute=1)
    async def daily_bgs(self):
        if datetime.now().strftime('%H:%M') == '16:00':
            await self.bb1984()
        else:
            pass

def setup(bot):
    bot.add_cog(Bigbrother(bot))
