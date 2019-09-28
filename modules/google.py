import discord, os, random, config
from datetime import datetime
from discord.ext import commands, tasks
import httplib2

from config import *
from data import *

import os
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


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


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
# Change that for your personal case
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Hermes'




class Google(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_credentials():
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    @commands.command(pass_context=True)
    @acces_oracle()
    async def farm(self, ctx, arg1):
        """
        Displays the lines from Phoenix's spreadsheet to know which geysers sites contains asked material
        """
        if not arg1:
            await ctx.send_message(ctx.message.channel, "Il faut indiquer le matériau en paramètre !")
            return

        materiau = str(arg1).lower()
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        spreadsheetId = '1HGKvQGqsP6UbElHY7XdfmsmD6CoCRxqXwjgB-kuU4Mw'
        rangeName = 'A3:AH100'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range=rangeName).execute()
        values = result.get('values', [])

        lignes_retour = {}

        ligne_actuelle = 1
        colonne_materiau = int(materiaux[materiau]['number'])

        message = ""

        if not values:
            message += 'Impossible de récupérer les valeurs.'
        else:
            for row in values:
                try:
                    if row[colonne_materiau] != "":
                        # Print columns A and E, which correspond to indices 0 and 4.
                        lignes_retour[ligne_actuelle] = {}
                        lignes_retour[ligne_actuelle] = row
                        ligne_actuelle = ligne_actuelle + 1
                except:
                    continue

        # On a nos lignes
        message = "**Liste des sites de geysers pour "
        message += materiau + "**"
        await ctx.send_message(ctx.message.channel, message)

        embed = discord.Embed(title="Localisation", description=str(materiaux[materiau]['location']), color=0x0000ff)
        await ctx.send_message(ctx.message.channel, embed=embed)

        for ligne_retour in lignes_retour.items():
            colonnes = ligne_retour[1]
            message = "**" + str(colonnes[1]) + "** - "
            message += "Astre : **" + str(colonnes[2]) + "**."
            message += " Coordonnées : **" + str(colonnes[3]) + "**\n"
            message += "**["
            message += str(colonnes[colonne_materiau])
            message += "%]** - "
            if colonnes[5] != '':
                message += "Distance de 32 MU : **"
                message += str(colonnes[5]) + " al** - "
            if colonnes[6] != '':
                message += "Distance de Pythéas : **"
                message += str(colonnes[6]) + " al** - "
            message += "Distance de l'étoile principale : **"
            message += str(colonnes[7]) + " sl**"

            embed = discord.Embed(title="", description=message, color=0x00ffaa)
            await ctx.send_message(ctx.message.channel, embed=embed)


def setup(bot):
    bot.add_cog(Google(bot))
