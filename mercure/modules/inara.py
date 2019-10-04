import discord, os
from discord.ext import commands
from main import acces_oracle, is_admin, _

import requests
import dateutil.parser
from datetime import datetime

from config import *
from data import *


class Inara(commands.Cog):
    def __init__(self, bot):
        if config['DEBUG']: print(_("Inara module loaded"))
        self.bot = bot
        self.inara_ranks = inara_ranks

    def cog_unload(self):
        if config['DEBUG']: print(_("Inara module unloaded"))

    @commands.command(pass_context=True)
    @acces_oracle()
    async def cg(self, ctx):
        """
        Displays the current CGs thanks to inara
        """
        if config['DEBUG']: print(_("cg command"))
        now = datetime.utcnow()
        iso8601_time = now.isoformat()
        json_for_inara = """
    {
        "header": {
            "appName": "%s",
            "appVersion": "0.1",
            "isDeveloped": true,
            "APIkey": "%s",
            "commanderName": "%s"
        },
        "events": [
            {
               "eventName": "getCommunityGoalsRecent",
               "eventTimestamp": "%s",
               "eventData": []
            }
        ]
    }""" % (config["inara_appname"], config["inara_api_key"], config["inara_cmdr_name"], iso8601_time)

        url_to_call = "https://inara.cz/inapi/v1/"

        message = ""

        try:
            r = requests.get(url_to_call, data=json_for_inara)
            informations = r.json()
        except:
            await ctx.send(_("Oops ! :crying_cat_face: "))
            return

        active_cgs = 0

        for cg in informations['events'][0]['eventData']:
            if not cg['isCompleted']:
                active_cgs += 1
                # D'abord le titre du CG à part
                message = "**" + cg["communitygoalName"] + "**"
                await ctx.send(message)

                # Ensuite, un embed avec les infos du cg
                embed = discord.Embed(title="", color=0x00ff00)
                embed.add_field(name=_("Starsystem"), value=cg["starsystemName"], inline=True)
                embed.add_field(name=_("Station"), value=cg["stationName"], inline=True)
                goal_expiry = dateutil.parser.parse(cg["goalExpiry"])
                embed.add_field(name=_("Expiration date"), value=goal_expiry.strftime(_("%d/%m/%Y at %H:%M")), inline=True)
                embed.add_field(name=_("Tier reached"), value=str(cg["tierReached"]) + "/" + str(cg["tierMax"]),
                                inline=True)
                embed.add_field(name="Contributors number", value=str(cg["contributorsNum"]), inline=True)
                embed.add_field(name="Total of contributions", value=str(cg['contributionsTotal']), inline=True)
                last_update = dateutil.parser.parse(cg['lastUpdate'])
                embed.set_footer(text=last_update.strftime(_("Updated on %d/%m/%Y at %H:%M")))
                await ctx.send(embed=embed)

                # Puis, un embed avec en description un blockquote le texte descriptif du cg
                message = "```" + cg['goalDescriptionText'] + "```"
                embed = discord.Embed(title=cg['goalObjectiveText'], description=message)
                await ctx.send(embed=embed)

        if active_cgs > 0:
            message = _("Your turn, Commanders !")
        else:
            message = _("No active CG, check back later")
        await ctx.send(message)

    @commands.command(pass_context=True)
    @acces_oracle()
    async def inara(self, ctx, *, arg1=""):
        """
        Displays the inara information about a commander
        """
        if config['DEBUG']: print(_("inara command"))
        # Si pas d'argument donné, on affiche juste le lien de la wing LGC
        if arg1 == "":
            embed = discord.Embed(title="", color=0x00ff00)
            embed.add_field(name=_("LGC Squadron on Inara"), value="<https://inara.cz/wing/280/>", inline=True)
            url = "http://guilde-cartographes.fr/INFORMATIONS/32MU_STARNEWS/wp-content/uploads/2016/09/LOGO_LGC.png"
            embed.set_thumbnail(url=url)
            await ctx.send(embed=embed)
            return


        cmdr_name = arg1
        now = datetime.utcnow()
        iso8601_time = now.isoformat()
        json_for_inara = """
    {
        "header": {
            "appName": "%s",
            "appVersion": "0.1",
            "isDeveloped": true,
            "APIkey": "%s",
            "commanderName": "%s"
        },
        "events": [
            {
                "eventName": "getCommanderProfile",
                "eventTimestamp": "%s",
                "eventData": {
                    "searchName": "%s"
                }
            }
        ]
    }""" % (config["inara_appname"], config["inara_api_key"], cmdr_name, iso8601_time, cmdr_name)
        url_to_call = "https://inara.cz/inapi/v1/"

        message = ""

        try:
            r = requests.get(url_to_call, data=json_for_inara)
            informations = r.json()
        except:
            await ctx.send(_("Inara API request : nope :crying_cat_face: "))
            return

        inara_data = informations['events'][0]['eventData']
        if config['DEBUG']: print(inara_data)

        try:
            message = _("**Informations on {commander_name}**").format(commander_name = inara_data['commanderName'])
            await ctx.send(message)
        except:
            message = _("**Informations on {commander_name}**").format(commander_name = inara_data['userName'])
            await ctx.send(message)

        try:
            if(inara_data['avatarImageURL']):
                embed = discord.Embed(title="")
                embed.set_thumbnail(url=inara_data['avatarImageURL'])
                await ctx.send(embed=embed)
        except:
            pass

        embed = discord.Embed(title=_("*Pilot's Federation ranks*"), color=0x00ff00)
        for data in inara_data['commanderRanksPilot']:
            progress = 100 * data['rankProgress']
            value = self.inara_ranks[data['rankName']][data['rankValue']]
            if progress != 0:
                value += " - " + str(progress) + "\%"
            embed.add_field(name=data['rankName'], value= value, inline=True)

        await ctx.send(embed=embed)

        embed = discord.Embed(title="", color=0x00ffff)

        embed.add_field(name=_("Allegiance"), value=_(inara_data['preferredAllegianceName']), inline=False)
        embed.add_field(name=_("Prefered game role"), value=inara_data['preferredGameRole'], inline=False)
        embed.add_field(name=_("Inara profile link"), value=inara_data['inaraURL'], inline=False)

        await ctx.send(embed=embed)

        embed = discord.Embed(title="*Informations d\'escadrille*", color=0x0000ff)

        embed.add_field(name=_("Wing name"), value=inara_data['commanderWing']['wingName'], inline=True)
        embed.add_field(name=_("Members count"), value=inara_data['commanderWing']['wingMembersCount'], inline=True)
        embed.add_field(name=_("Wing member rank"), value=inara_data['commanderWing']['wingMemberRank'], inline=True)
        embed.add_field(name=_("Inara squadron link"), value=inara_data['commanderWing']['inaraURL'], inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Inara(bot))