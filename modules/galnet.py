import discord, os, random, config
from datetime import datetime
from discord.ext import commands

from html2text import html2text
import requests
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


class Galnet(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @acces_oracle()
    async def galnet(self, ctx, arg=None):
        """
        Display today's galnet articles if there are any, or the articles for the date passed as a parameter
        The required format is DD-MMM-YYYY like 03-DEC-3303
        """
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
            output += "** Pas d'article trouvé ce jour : " + jour + "**\n"

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
                    await ctx.send_message(ctx.message.channel, sending)
            output += "\n"

        if output.strip() != "":
            await ctx.send_message(ctx.message.channel, output)


def setup(client):
    client.add_cog(Galnet(client))
