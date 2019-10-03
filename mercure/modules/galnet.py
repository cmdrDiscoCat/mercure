import discord, os, random, config
from discord.ext import commands
from main import acces_oracle, is_admin

from html2text import html2text
import requests
from datetime import datetime
from bs4 import BeautifulSoup

from config import *
from data import *

import gettext

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locales')
translate = gettext.translation('mercure', localedir, languages=[config['LANGUAGE']], fallback=True)
_ = translate.gettext


class Galnet(commands.Cog):
    def __init__(self, bot):
        if config['DEBUG']: print(_("Galnet module loaded"))
        self.bot = bot

    def cog_unload(self):
        if config['DEBUG']: print(_("Galnet module unloaded"))

    @commands.command(pass_context=True)
    @acces_oracle()
    async def galnet(self, ctx, arg=None):
        """
        Display today's galnet articles if there are any, or the articles for the date passed as a parameter
        The required format is DD-MMM-YYYY like 03-DEC-3303
        """
        if config['DEBUG']: print(_("galnet command"))
        now = datetime.utcnow()
        month = str(now.strftime("%b")).upper()
        year = str(int(now.strftime("%Y")) + 1286)

        if arg is None:
            jour = datetime.utcnow().strftime("%d-") + month + "-" + year
        else:
            jour = arg

        output = ""

        r = requests.get("https://community.elitedangerous.com/fr/galnet/" + jour)
        soup = BeautifulSoup(r.text, "html.parser")

        output += "Date : " + jour + "\n"
        output += "--------------------\n"

        for element in soup.find_all('div', attrs={'class': 'article'}):

            # On est dans le div d'un article, on affiche les belles choses
            titre = element.h3.get_text()
            output += "\n**" + titre + "**\n\n"

            for div in element.find_all('div', attrs={'class': 'i_right'}):
                div.decompose()

            for div in element.find_all('h3'):
                div.decompose()

            cleaned_text = html2text(str(element))
            output += cleaned_text
            output += "--------------------\n"

        if output == "":
            output += _("** No article found for that date : ") + jour + "**\n"

        messages = output.split('\n')

        output = ""
        for message in messages:
            if message.strip() != "":
                if len(output) < 1800:
                    output += message
                else:
                    output += message
                    sending = output
                    output = ""
                    await ctx.send(sending)
            output += "\n"

        if output.strip() != "":
            await ctx.send(output)


def setup(bot):
    bot.add_cog(Galnet(bot))
