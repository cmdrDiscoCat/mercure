import discord, os
from discord.ext import commands
from main import acces_oracle, is_admin, _
from config import *
from data import *
from farm import *

import requests
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup


class Edsm(commands.Cog):
    def __init__(self, bot):
        if config['DEBUG']: print(_("Edsm module loaded"))
        self.bot = bot
        self.translations = translations

    def cog_unload(self):
        if config['DEBUG']: print(_("Edsm module unloaded"))

    @commands.command(pass_context=True, aliases=[_('ed')])
    @acces_oracle()
    async def edsm_ed(self, ctx):
        """
        Displays the edsm data about elite dangerous servers status
        """
        if config['DEBUG']: print(_("ed command"))
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

        embed = discord.Embed(title=_("Status message returned by the Elite Dangerous servers"),
                              description="```" + informations['message'] + "```", color=color)
        embed.set_footer(text=_("Last updated on : ") + informations['lastUpdate'])
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=[_('traffic')])
    @acces_oracle()
    async def edsm_traffic(self, ctx, *, arg):
        """
        Displays the edsm data about traffic in a star system
        """
        if config['DEBUG']: print(_("traffic command"))
        system = urllib.parse.quote(arg)
        url_to_call = "https://www.edsm.net/api-system-v1/traffic?systemName=" + system

        r = requests.get(url_to_call)
        informations = r.json()

        await ctx.send(_("***Traffic information for the {system} system***")
                       .format(system=informations["name"]))

        embed = discord.Embed(title="", color=0x000000)
        embed.add_field(name=_("Total traffic since the discovery of the system"),
                        value=informations["traffic"]["total"],
                        inline=False)
        embed.add_field(name=_("Last week's traffic"), value=informations["traffic"]["week"], inline=False)
        embed.add_field(name=_("Last day's traffic"), value=informations["traffic"]["day"], inline=False)
        await ctx.send(embed=embed)

        if informations["traffic"]["day"] > 0:
            await ctx.send(_("***Last 24 hours' detail, by ship***"))
            embed = discord.Embed(title="", color=0x00ff00)
            for name, count in informations['breakdown'].items():
                embed.add_field(name=name, value=count, inline=False)
            await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=[_("stations")])
    @acces_oracle()
    async def edsm_stations(self, ctx, *, arg):
        """
        Displays the edsm data about a star system
        """
        if config['DEBUG']: print(_("stations command"))
        system = urllib.parse.quote(arg)
        url_to_call = "https://www.edsm.net/api-system-v1/stations?systemName=" + system

        r = requests.get(url_to_call)
        informations = r.json()

        await ctx.send(_("***Stations in the {system} system***").format(system=informations["name"]))

        if informations['stations']:
            # for each station, an embed with all the intel
            for station in informations['stations']:
                await ctx.send(_("```{station} - Type {type}```")
                               .format(station=station["name"],type=station["type"]))
                embed = discord.Embed(title="", color=0x00ffff)
                try:
                    embed.add_field(name=_("Distance to Arrival"),
                                    value=str(round(station["distanceToArrival"], 1)) + " sl", inline=False)
                except:
                    pass

                embed.add_field(name=_("Allegiance"), value=self.translations[station["allegiance"]], inline=True)
                embed.add_field(name=_("Government"), value=self.translations[station["government"]], inline=True)
                embed.add_field(name=_("Economy"), value=self.translations[station["economy"]], inline=True)

                yes_checkbox = _("Yes")
                no_checkbox = _("No")
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

                embed.add_field(name=_("Market"), value=market, inline=True)
                embed.add_field(name=_("Shipyard"), value=shipyard, inline=True)
                embed.add_field(name=_("Equipment"), value=equipment, inline=True)

                if not station['otherServices']:
                    pass
                else:
                    other_services = ""
                    for service in station['otherServices']:
                        other_services += self.translations[service] + " / "
                    other_services = other_services.rstrip(' / ')
                    embed.add_field(name=_("Other services"), value=other_services, inline=True)

                embed.add_field(name=_("Controlling Faction"),
                                value=station['controllingFaction']['name'], inline=False)

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

    @commands.command(pass_context=True, aliases=[_('system')])
    @acces_oracle()
    async def edsm_system(self, ctx, *, arg):
        """
        Displays the edsm data about a star system
        """
        if config['DEBUG']: print(_("system command called with {system}").format(system=str(arg)))
        system = urllib.parse.quote(arg)
        url_to_call = "https://www.edsm.net/api-v1/system?systemName="
        url_to_call += system+"&showId=1&showCoordinates=1&showPermit=1&showInformation=1&showPrimaryStar=1"

        r = requests.get(url_to_call)
        informations = r.json()

        if informations["name"]:
            await ctx.send(_("***Summary of the {system} system***").format(system=informations["name"]))

            if informations["coords"]["x"]:
                desc = "x :" + str(informations["coords"]["x"]) \
                       + ' / y : ' + str(informations["coords"]["y"]) \
                       + ' / z :  ' + str(informations["coords"]["z"])
                embed = discord.Embed(title=_("Coordinates"), description = desc)
                await ctx.send(embed=embed)

            embed = discord.Embed(title="", color=0x00ff00)
            embed.add_field(name=_("Controlling Faction"), value=informations["information"]["faction"],
                            inline=False)
            await ctx.send(embed=embed)

            embed = discord.Embed(title="", color=0x00ffff)
            embed.add_field(name=_("Allegiance"),
                            value=_(self.translations[informations["information"]["allegiance"]]), inline=True)
            embed.add_field(name=_("Government"),
                            value=_(self.translations[informations["information"]["government"]]), inline=True)
            embed.add_field(name=_("State"),
                            value=_(self.translations[informations["information"]["factionState"]]), inline=True)
            embed.add_field(name=_("Population"),
                            value=informations["information"]["population"], inline=True)

            try:
                embed.add_field(name=_("Mineral reserves"),
                                value=informations["information"]["reserve"], inline=True)
            except:
                embed.add_field(name=_("Mineral reserves"),
                                value=_("None"), inline=True)

            embed.add_field(name=_("Security and Economy"),
                            value=_(self.translations[informations["information"]["security"]])
                                  + " / " + _(self.translations[informations["information"]["economy"]]),
                            inline=True)
            await ctx.send(embed=embed)

            if informations["primaryStar"]:
                scoopable = ""
                if informations["primaryStar"]["isScoopable"]:
                    scoopable = "Scoopable"
                else:
                    scoopable = "Not scoopable"
                desc = _("{starName} / Spectral Type : {starType} / {fuelscoop}")\
                    .format(starName=str(informations["primaryStar"]["name"]),
                            starType=str(informations["primaryStar"]["type"]),
                            fuelscoop=scoopable)
                embed = discord.Embed(title=_("Main Star"), description = desc, color=0xffaaaa)
                await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=[_('oracle')])
    @acces_oracle()
    async def edsm_oracle(self, ctx):
        """
        Displays all the links to follow our influence in the star systems we're in
        """
        if config['DEBUG']: print(_("oracle command"))
        desc = "* EDSM : <https://www.edsm.net/en/faction/id/8172/name/LGC+-+Cartographers%27s+Guild>\n" \
               "* EDDB : <https://eddb.io/faction/75388>\n\n"

        titre = _("***LGC Systems' states***")
        await ctx.send(titre)

        embed = discord.Embed(title=_("Bubble"), description=desc, color=0x00ff00)
        await ctx.send(embed=embed)

        desc = ""
        desc = "* EDSM : <https://www.edsm.net/en/faction/id/21093/name/LGC+-+Colonia+Cartographers%27+Guild> \n" \
               "* EDDB : <https://eddb.io/faction/75524> \n"

        embed = discord.Embed(title=_("Colonia"), description=desc, color=0x147119)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=[_('influence')])
    @acces_oracle()
    async def edsm_influence(self, ctx, *, arg):
        """
        Displays the factions present in asked start system and their influence percentage
        """
        if config['DEBUG']: print(_("influence command called with {system}").format(system=urllib.parse.quote(arg)))

        system_display = arg
        system = urllib.parse.quote(arg)
        url_to_call = "https://www.edsm.net/api-system-v1/factions?systemName="+system

        r = requests.get(url_to_call)
        informations = r.json()

        last_update = 0
        information_embed = ""

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

                information_embed += "[{:.1%}".format(faction['influence']) + "]\t" + nom_faction
                information_embed += " | " + _(self.translations[faction['state']])
                information_embed += " | " + _(self.translations[faction['allegiance']])
                information_embed += " | " + _(self.translations[faction['government']])
                information_embed += " " + player_faction + "\n"
                if faction['lastUpdate'] > last_update:
                    last_update = faction['lastUpdate']

            # We convert the last timestamp to a date
            last_update = datetime.fromtimestamp(faction['lastUpdate'])
            header_embed = _("***Influences in the {system} system").format(system=informations['name'])
            if last_update != 0:
                header_embed += _("*** on the ***{date}*** \n").format(date=last_update.strftime("%d/%m/%Y at %Hh%M"))
            else:
                header_embed += _("*** as of today *** \n")
            header_embed += "<https://www.edsm.net/en/system/id/"
            header_embed += str(informations['id']) + "/name/" + urllib.parse.quote_plus(arg) + ">\n"

            await ctx.send(header_embed)
            embed = discord.Embed(title="", description = information_embed, color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            await ctx.send(_("No system found with the name {system} :crying_cat_face:").format(system=system_display))

    @commands.command(pass_context=True, aliases=[_('spy')])
    @acces_oracle()
    async def edsm_spy(self, ctx, *, arg):
        """
        Displays the last known location in EDSM for a commander
        """
        if config['DEBUG']: print(_("spy command called with {cmdrname}").format(cmdrname=urllib.parse.quote(arg)))
        cmdr_name = urllib.parse.quote(arg)
        url_to_call = "https://www.edsm.net/api-logs-v1/get-position?commanderName=" + cmdr_name
        try:
            r = requests.get(url_to_call)
            informations = r.json()
            information_embed = _("My spies told me that CMDR **{cmdr}** was last seen in **{system}**")\
                                    .format(cmdr=str(arg).title(),
                                            system=informations['system'])
            information_embed += _(" on that day : **{date}**.\n\n").format(date=informations['date'])
            information_embed += _("For more information, spy that CMDR there : <{url}>")\
                .format(url=informations['url'])
            await ctx.send(information_embed)
        except:
            await ctx.send("Oops ! :crying_cat_face: ")

    @commands.command(pass_context=True, aliases=[_('faction')])
    @acces_oracle()
    async def edsm_faction(self, ctx, *, arg):
        """ One day, this will be a thing returning the systems where a faction is present """
        if config['DEBUG']: print(_("faction command called with {cmdrname}").format(cmdrname=urllib.parse.quote(arg)))
        system = urllib.parse.quote(arg)
        url_to_call = "https://www.edsm.net/api-system-v1/factions?systemName=" + system
        try:
            r = requests.get(url_to_call)
            informations = r.json()
        except:
            await ctx.send("Oops ! :crying_cat_face: ")

    def edsm_farm_body_search(self, ctx, material, system, volcanism_id):
        """
        this function returns a dict of any body meeting the material, system and volcanism id asked
        :param ctx:
        :param material:
        :param system:
        :param volcanism_id:
        :return:
        """
        if config['DEBUG']: print(_("farm body function called with {volcanism_id}").format(volcanism_id=str(volcanism_id)))

        # Let's build the url request for edsm
        url_to_call = "https://www.edsm.net/en/search/bodies/index/group/"+str(EDSM_BODIES)+"/"
        url_to_call += "cmdrPosition/"+system+"/"
        url_to_call += "material/"+str(minerals[material])+"/"
        url_to_call += "materialProportion"+str(minerals[material])+"/1%2C100/"
        url_to_call += "distanceToArrival/0%2C7000/"
        url_to_call += "gravity/0.1%2C2.5/"
        url_to_call += "isLandable/1/"
        url_to_call += "radius/100/"
        url_to_call += "sortBy/distanceCMDR/"
        url_to_call += "volcanism/"+str(volcanism_id)+"/"

        if config['DEBUG']: print(url_to_call)

        try:
            r = requests.get(url_to_call)
        except:
            ctx.send("Oops ! :crying_cat_face: ")

        # Now, we have a returned page, we seek system links to know if there are result
        soup = BeautifulSoup(r.text, "html.parser")

        bodies = {}

        # this works too but it's less elegant
        # systems_links = soup.findAll('a', href=re.compile('^/galaxy-starsystem/'))
        row = 1
        tbody = soup.find('tbody')
        for tr in tbody.find_all('tr'):
            if row < 6:
                col = 0
                bodies[row] = {}
                for td in tr.find_all('td'):
                    if col == 1:
                        bodies[row]["name"] = td.a.get_text()
                    if col == 3:
                        bodies[row]["gravity"] = td.get_text().strip()
                    if col == 4:
                        bodies[row]["distance"] = td.get_text().strip()
                    col += 1
                row += 1

        if config['DEBUG']: print(
            _("farm body function returned for {volcanism_id} :").format(volcanism_id=str(volcanism_id)))
        if config['DEBUG']: print(bodies)
        return bodies

    @commands.command(pass_context=True, aliases=[_('farm')])
    @acces_oracle()
    async def edsm_farm(self, ctx, material, *, system):
        """
        Launches a search, volcanism type by volcanism type, to find a body near system with said material AND geology
        """
        if config['DEBUG']: print(_("farm command"))
        if not material:
            await ctx.send(_("You must specify a material !"))
            return

        if not system:
            await ctx.send(_("You must specify a system !"))
            return

        material = str(material).lower()
        system_display = system
        system = urllib.parse.quote(system)
        # As this is gonna take time, we tell them to be patient
        waiting_message = await ctx.send(_("You asked for the mineral {} near {}. Please wait while I'm searching...")
                       .format(material, system_display))

        # Now, for each volcanism type above 0 , we call our function returning a list of the bodies matching the search
        for volcanism_id in volcanism_types.keys():
            if volcanism_id > 0:
                bodies = self.edsm_farm_body_search(ctx, material, system, volcanism_id)
                if len(bodies) > 0:
                    await waiting_message.delete()
                    await ctx.send(_("Here are the results for some {} near {}.").format(material, system_display))
                    for body_id, body in bodies.items():
                        embed = discord.Embed(title="", color=0x00ffff)
                        embed.add_field(name=_("Body"),
                                        value=body['name'], inline=True)
                        embed.add_field(name=_("Gravity"),
                                        value=body['gravity'], inline=True)
                        embed.add_field(name=_("Distance from {}").format(str(system_display).capitalize()),
                                        value=body['distance'], inline=True)
                        await ctx.send(embed=embed)
                    return

        await ctx.send(_("No results... :crying_cat_face: "))


def setup(bot):
    bot.add_cog(Edsm(bot))
