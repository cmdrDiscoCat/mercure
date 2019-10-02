import discord
from discord.ext import commands
from main import acces_oracle, is_admin

from config import *
from data import *

import requests
import urllib.parse
from datetime import datetime


class Edsm(commands.Cog):
    def __init__(self, bot):
        if config['DEBUG']: print("Cog Edsm initialisé")
        self.bot = bot

    @commands.command(pass_context=True)
    @acces_oracle()
    async def ed(self, ctx):
        """
        Displays the edsm data about elite dangerous servers status
        """
        if config['DEBUG']: print("Commande ed")
        url_to_call = "https://www.edsm.net/api-status-v1/elite-server"

        r = requests.get(url_to_call)
        informations = r.json()

        if informations['type'] == 'success':
            color = 0x00ff00
        elif informations['type'] == 'warning':
            color = 0xffff00
        elif informations['type'] == 'danger':
            color = 0xff0000
        else:
            color = 0x000000

        embed = discord.Embed(title="Message de statut retourné par les serveurs Elite Dangerous",
                              description="```" + informations['message'] + "```", color=color)
        embed.set_footer(text="Date de dernière mise à jour : " + informations['lastUpdate'])
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @acces_oracle()
    async def trafic(self, ctx, *, arg):
        """
        Displays the edsm data about traffic in a star system
        """
        if config['DEBUG']: print("Commande trafic")
        system = urllib.parse.quote(arg)
        url_to_call = "https://www.edsm.net/api-system-v1/traffic?systemName=" + system

        r = requests.get(url_to_call)
        informations = r.json()

        await ctx.send_message(ctx.message.channel,
                               "***Informations sur le trafic dans le système " + informations["name"] + "***")

        embed = discord.Embed(title="", color=0x000000)
        embed.add_field(name="Trafic total depuis la découverte du système", value=informations["traffic"]["total"],
                        inline=False)
        embed.add_field(name="Trafic de la dernière semaine", value=informations["traffic"]["week"], inline=False)
        embed.add_field(name="Trafic des dernières 24h", value=informations["traffic"]["day"], inline=False)
        await ctx.send(embed=embed)

        if informations["traffic"]["day"] > 0:
            await ctx.send("***Détail par vaisseau sur les dernières 24 heures***")
            embed = discord.Embed(title="", color=0x00ff00)
            for name, count in informations['breakdown'].items():
                embed.add_field(name=name, value=count, inline=False)
            await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @acces_oracle()
    async def stations(self, ctx, *, arg):
        """
        Displays the edsm data about a star system
        """
        if config['DEBUG']: print("Commande stations")
        system = urllib.parse.quote(arg)
        url_to_call = "https://www.edsm.net/api-system-v1/stations?systemName=" + system

        r = requests.get(url_to_call)
        informations = r.json()

        await ctx.send("***Stations du système " + informations["name"] + "***")

        if informations['stations']:
            # for each station, an embed with all the intel
            for station in informations['stations']:
                await ctx.send_message(ctx.message.channel,
                                       "```" + station["name"] + " de type " + station["type"] + "```")

                embed = discord.Embed(title="", color=0x00ffff)
                try:
                    embed.add_field(name="Distance depuis l'arrivée dans le système",
                                    value=str(round(station["distanceToArrival"], 1)) + " sl", inline=False)
                except:
                    pass

                embed.add_field(name="Allégeance", value=traduction[station["allegiance"]], inline=True)
                embed.add_field(name="Gouvernement", value=traduction[station["government"]], inline=True)
                embed.add_field(name="Economie", value=traduction[station["economy"]], inline=True)

                yes_checkbox = "Oui"
                no_checkbox = "Non"
                if station["haveMarket"]:
                    market = yes_checkbox
                else:
                    market = no_checkbox

                if station["haveShipyard"]:
                    shipyard = yes_checkbox
                else:
                    shipyard = no_checkbox

                if station["haveOutfitting"]:
                    equipment = yes_checkbox
                else:
                    equipment = no_checkbox

                embed.add_field(name="Marché", value=market, inline=True)
                embed.add_field(name="Chantier naval", value=shipyard, inline=True)
                embed.add_field(name="Equipement", value=equipment, inline=True)

                if not station['otherServices']:
                    pass
                else:
                    other_services = ""
                    for service in station['otherServices']:
                        other_services += traduction[service] + " / "
                    other_services = other_services.rstrip(' / ')
                    embed.add_field(name="Autres services", value=other_services, inline=True)

                embed.add_field(name="Faction dirigeante", value=station['controllingFaction']['name'], inline=False)

                url = ""
                if station['type'] == 'Coriolis Starport':
                    url = "http://edassets.org/img/stations/Coriolis.png"
                if station['type'] == 'Ocellus Starport':
                    url = "http://edassets.org/img/stations/Ocellus.png"
                if station['type'] == 'Orbis Starport':
                    url = "http://edassets.org/img/stations/Orbis.png"
                if station['type'] == 'Asteroid base':
                    url = "http://edassets.org/img/stations/Asteroid_Station_Icon.png"
                if station['type'] == 'Mega ship':
                    url = "http://edassets.org/img/stations/Mega-Ship_Icon.png"
                if station['type'] == "Outpost":
                    url = "http://edassets.org/img/stations/Outpost.png"
                if station['type'] == "Planetary Outpost":
                    url = "http://edassets.org/img/settlements/settlement_pm.png"

                embed.set_thumbnail(url=url)
                await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @acces_oracle()
    async def systeme(self, ctx, *, arg):
        """
        Displays the edsm data about a star system
        """
        if config['DEBUG']: print("Commande systeme")
        system = urllib.parse.quote(arg)
        url_to_call = "https://www.edsm.net/api-v1/system?systemName="
        url_to_call += system+"&showId=1&showCoordinates=1&showPermit=1&showInformation=1&showPrimaryStar=1"

        r = requests.get(url_to_call)
        informations = r.json()

        if informations["name"]:
            await ctx.send("***Résumé du système " + informations["name"]+"***")

            if informations["coords"]["x"]:
                desc = "x :" + str(informations["coords"]["x"]) \
                       + ' / y : ' + str(informations["coords"]["y"]) \
                       + ' / z :  ' + str(informations["coords"]["z"])
                embed = discord.Embed(title="Coordonnées", description = desc)
                await ctx.send(embed=embed)

            embed = discord.Embed(title="", color=0x00ff00)
            embed.add_field(name="Faction dirigeante", value=informations["information"]["faction"], inline=False)
            await ctx.send(embed=embed)

            embed = discord.Embed(title="", color=0x00ffff)
            embed.add_field(name="Allégeance", value=traduction[informations["information"]["allegiance"]], inline=True)
            embed.add_field(name="Gouvernement", value=traduction[informations["information"]["government"]], inline=True)
            embed.add_field(name="Etat", value=traduction[informations["information"]["factionState"]], inline=True)
            embed.add_field(name="Population", value=informations["information"]["population"], inline=True)

            try:
                embed.add_field(name="Réserves minérales", value=informations["information"]["reserve"], inline=True)
            except:
                embed.add_field(name="Réserves minérales", value="Aucune", inline=True)

            embed.add_field(name="Sécurité et Economie", value=traduction[informations["information"]["security"]] + " / " + informations["information"]["economy"], inline=True)
            await ctx.send(embed=embed)

            if informations["primaryStar"]:
                scoopable = ""
                if informations["primaryStar"]["isScoopable"]:
                    scoopable = "Scoopable"
                else:
                    scoopable = "Non scoopable"
                desc = str(informations["primaryStar"]["name"])+ " / Type spectral : " \
                       + str(informations["primaryStar"]["type"]) + " / "+ scoopable
                embed = discord.Embed(title="Etoile principale", description = desc, color=0xffaaaa)
                await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @acces_oracle()
    async def oracle(self, ctx):
        """
        Displays all the links to follow our influence in the star systems we're in
        """
        if config['DEBUG']: print("Commande oracle")
        desc = "* EDSM : <https://www.edsm.net/en/faction/id/8172/name/LGC+-+Cartographers%27s+Guild>\n" \
               "* EDDB : <https://eddb.io/faction/75388>\n\n"

        titre = "***Etat des systèmes LGC***"
        await ctx.send(titre)

        embed = discord.Embed(title="Bulle", description=desc, color=0x00ff00)
        await ctx.send(embed=embed)

        desc = ""
        desc = "* EDSM : <https://www.edsm.net/en/faction/id/21093/name/LGC+-+Colonia+Cartographers%27+Guild> \n" \
               "* EDDB : <https://eddb.io/faction/75524> \n"

        embed = discord.Embed(title="Colonia", description=desc, color=0x147119)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @acces_oracle()
    async def influence(self, ctx, *, arg):
        """
        Displays the factions present in asked start system and their influence percentage
        """
        if config['DEBUG']: print("Commande influence avec l'argument "+str(arg))

        system = urllib.parse.quote(arg)
        url_to_call = "https://www.edsm.net/api-system-v1/factions?systemName="+system

        r = requests.get(url_to_call)
        informations = r.json()

        last_update = 0
        information_block = ""

        # If a system was found corresponding to the one asked
        if informations.get('factions'):
            for faction in informations['factions']:
                if faction['name'] == informations['controllingFaction']['name']:
                    is_controlling = 1
                    nom_faction = "**" + faction['name'] + "**"
                else:
                    is_controlling = 0
                    nom_faction = faction['name']

                if faction['isPlayer']:
                    player_faction = ":grinning:"
                else:
                    player_faction = ":robot:"

                information_block += "[{:.1%}".format(faction['influence']) + "]\t" + nom_faction
                information_block += " | " + traduction[faction['state']]
                information_block += " | " + traduction[faction['allegiance']]
                information_block += " | " + traduction[faction['government']]
                information_block += " " + player_faction + "\n"
                if faction['lastUpdate'] > last_update:
                    last_update = faction['lastUpdate']

            # We convert the last timestamp to a date
            last_update = datetime.fromtimestamp(faction['lastUpdate'])
            bloc_entete = "***Influences dans le système " + informations['name']
            if last_update != 0:
                bloc_entete += "*** en date du ***"+last_update.strftime("%d/%m/%Y à %Hh%M")+"*** \n"
            else:
                bloc_entete += "*** en date d'aujourd'hui *** \n"
            bloc_entete += "<https://www.edsm.net/en/system/id/"+str(informations['id'])+"/name/"+urllib.parse.quote_plus(arg)+">\n"

            await ctx.send(bloc_entete)
            embed = discord.Embed(title="", description = information_block, color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Aucun système trouvé avec ce nom ! :crying_cat_face:")

    @commands.command(pass_context=True)
    @acces_oracle()
    async def espionner(self, ctx, *, arg):
        """
        Displays the last known location in EDSM for a commander
        """
        if config['DEBUG']: print("Commande espionner")
        cmdr_name = urllib.parse.quote(arg)
        url_to_call = "https://www.edsm.net/api-logs-v1/get-position?commanderName=" + cmdr_name
        try:
            r = requests.get(url_to_call)
            informations = r.json()
            information_block = "D'après mes espions, **" + str(arg).title() + "** a été vu·e à **" + informations[
                'system']
            information_block += "** ce jour : **" + informations['date'] + "**.\n\n"
            information_block += "Pour en savoir plus, espionnez cette personne ici : <" + informations['url'] + ">"
            await ctx.send(information_block)
        except:
            await ctx.send("Oops ! :crying_cat_face: ")

    @commands.command(pass_context=True)
    @acces_oracle()
    async def faction(self, ctx, *, arg):
        """ One day, this will be a thing """
        if config['DEBUG']: print("Commande faction")
        system = urllib.parse.quote(arg)
        url_to_call = "https://www.edsm.net/api-system-v1/factions?systemName=" + system
        try:
            r = requests.get(url_to_call)
            informations = r.json()
        except:
            await ctx.send("Oops ! :crying_cat_face: ")


def setup(bot):
    bot.add_cog(Edsm(bot))
