import discord
from discord.ext import commands

import requests
import dateutil.parser
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
        if(str(ctx.message.channel) == 'oracle'):
            if ctx.message.author.id in admin_ids:
                return True
            else:
                return False
        else:
            return True
    return commands.check(verifier_droits_oracle)

class Inara(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @acces_oracle()
    async def cg(self, ctx):
        """
        Displays the current CGs thanks to inara
        """
        now = datetime.utcnow()
        iso8601_time = now.isoformat()
        json_for_inara = """
    {
        "header": {
            "appName": "%s",
            "appVersion": "0.1",
            "isDeveloped": true,
            "APIkey": "%s",
            "commanderName": "Disco Cat"
        },
        "events": [
            {
               "eventName": "getCommunityGoalsRecent",
               "eventTimestamp": "%s",
               "eventData": []
            }
        ]
    }""" % (config["inara_appname"], config["inara_api_key"],iso8601_time)

        url_to_call = "https://inara.cz/inapi/v1/"

        message = ""

        try:
            r = requests.get(url_to_call, data=json_for_inara)
            informations = r.json()
        except:
            await ctx.send_message(ctx.message.channel, "Oops, problème droit devant ! :crying_cat_face: ")
            return

        try:
            for cg in informations['events'][0]['eventData']:
                # D'abord le titre du CG à part
                message = "**" + cg["communitygoalName"] + "**"
                await ctx.send_message(ctx.message.channel, message)

                # Ensuite, un embed avec les infos du cg
                if cg['isCompleted'] == False:
                    couleur = 0x00ff00
                else:
                    couleur = 0xff0000

                embed = discord.Embed(title="", color=couleur)
                embed.add_field(name="Système", value=cg["starsystemName"], inline=True)
                embed.add_field(name="Station", value=cg["stationName"], inline=True)
                date_expiration = dateutil.parser.parse(cg["goalExpiry"])
                embed.add_field(name="Expiration", value=date_expiration.strftime("%d/%m/%Y à %H:%M"), inline=True)
                embed.add_field(name="Rang atteint", value=str(cg["tierReached"]) + "/" + str(cg["tierMax"]),
                                inline=True)
                embed.add_field(name="Nombre de participant(e)s", value=str(cg["contributorsNum"]), inline=True)
                embed.add_field(name="Contribution totale", value=str(cg['contributionsTotal']), inline=True)
                last_update = dateutil.parser.parse(cg['lastUpdate'])
                embed.set_footer(text=last_update.strftime("Mis à jour le %d/%m/%Y à %H:%M"))
                await ctx.send_message(ctx.message.channel, embed=embed)

                # Puis, un embed avec en description un blockquote le texte descriptif du cg
                message = "```" + cg['goalDescriptionText'] + "```"
                embed = discord.Embed(title=cg['goalObjectiveText'], description=message)
                await ctx.send_message(ctx.message.channel, embed=embed)
        except:
            await ctx.send_message(ctx.message.channel, "Oops, problème droit devant ! :crying_cat_face: ")
            return

        message = "A vous de jouer pilotes !"
        await ctx.send_message(ctx.message.channel, message)


    @commands.command(pass_context=True)
    @acces_oracle()
    async def inara(self, ctx, *, arg1=""):
        """
        Displays the inara information about a commander
        """
        # Si pas d'argument donné, on affiche juste le lien de la wing LGC
        if arg1 == "":
            embed = discord.Embed(title="", color=0x00ff00)
            embed.add_field(name="Escadrille LGC sur Inara", value="<https://inara.cz/wing/280/>", inline=True)
            url = "http://guilde-cartographes.fr/INFORMATIONS/32MU_STARNEWS/wp-content/uploads/2016/09/LOGO_LGC.png"
            embed.set_thumbnail(url=url)
            await ctx.send_message(ctx.message.channel, embed=embed)
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
            await ctx.send_message(ctx.message.channel, "Requête à Inara : nope :crying_cat_face: ")
            return

        donnees = informations['events'][0]['eventData']
        print(donnees)

        try:
            message = "**Informations sur " + donnees['commanderName'] + "**"
            await ctx.send_message(ctx.message.channel, message)
        except:
            message = "**Informations sur " + donnees['userName'] + "**"
            await ctx.send_message(ctx.message.channel, message)

        try:
            if(donnees['avatarImageURL']):
                embed = discord.Embed(title="")
                embed.set_thumbnail(url=donnees['avatarImageURL'])
                await ctx.send_message(ctx.message.channel, embed=embed)
        except:
            pass

        embed = discord.Embed(title="*Rangs de la Fédération des Pilotes*", color=0x00ff00)
        for donnee in donnees['commanderRanksPilot']:
            progression = 100 * donnee['rankProgress']
            valeur = inara_ranks[donnee['rankName']][donnee['rankValue']]
            if progression != 0:
                valeur += " - " + str(progression) + "\%"
            embed.add_field(name=donnee['rankName'], value= valeur, inline=True)

        await ctx.send_message(ctx.message.channel, embed=embed)

        embed = discord.Embed(title="", color=0x00ffff)

        embed.add_field(name="Allégeance", value=donnees['preferredAllegianceName'], inline=False)
        embed.add_field(name="Rôle de préférence", value=donnees['preferredGameRole'], inline=False)
        embed.add_field(name="Lien du profil", value=donnees['inaraURL'], inline=False)

        await ctx.send_message(ctx.message.channel, embed=embed)

        embed = discord.Embed(title="*Informations d\'escadrille*", color=0x0000ff)

        embed.add_field(name="Nom", value=donnees['commanderWing']['wingName'], inline=True)
        embed.add_field(name="Nombre de pilotes", value=donnees['commanderWing']['wingMembersCount'], inline=True)
        embed.add_field(name="Rang dans l'escadrille", value=donnees['commanderWing']['wingMemberRank'], inline=True)
        embed.add_field(name="Lien de l'escadrille", value=donnees['commanderWing']['inaraURL'], inline=True)

        await ctx.send_message(ctx.message.channel, embed=embed)


def setup(bot):
    bot.add_cog(Inara(bot))