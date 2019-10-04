import discord, os
from discord.ext import commands, tasks
from main import acces_oracle, is_admin, _
from config import *
from data import *

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
# Change that for your personal case
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Mercure'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

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


class Google(commands.Cog):
    def __init__(self, bot):
        if config['DEBUG']: print(_("Google module loaded"))
        self.bot = bot

    def cog_unload(self):
        if config['DEBUG']: print(_("Google module unloaded"))

    @commands.command(pass_context=True)
    @acces_oracle()
    async def farm(self, ctx, arg1):
        """
        Displays the lines from Phoenix's spreadsheet to know which geysers sites contains asked material
        """
        if config['DEBUG']: print(_("farm command"))
        if not arg1:
            await ctx.send(_("You must specify a material !"))
            return

        material = str(arg1).lower()
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        discovery_url = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discovery_url)

        spreadsheet_id = '1HGKvQGqsP6UbElHY7XdfmsmD6CoCRxqXwjgB-kuU4Mw'
        range_name = 'A3:AH100'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])

        return_lines = {}

        current_line = 1
        material_column = int(materials[material]['number'])

        message = ""

        if not values:
            message += _("Can't get data.")
        else:
            for row in values:
                try:
                    if row[material_column] != "":
                        # Print columns A and E, which correspond to indices 0 and 4.
                        return_lines[current_line] = {}
                        return_lines[current_line] = row
                        current_line = current_line + 1
                except:
                    continue

        # We got our lines
        message = _("**Geyser sites' list for {material}**").format(material=material)
        await ctx.send(message)

        embed = discord.Embed(title=_("Location"), description=str(materials[material]['location']), color=0x0000ff)
        await ctx.send(embed=embed)

        # For each line, we check the columns for the values we seek and build the message we'll return
        for return_line in return_lines.items():
            columns = return_line[1]
            message = "**" + str(columns[1]) + "** - "
            message += _("Body : **") + str(columns[2]) + "**."
            message += _(" Coordinates : **") + str(columns[3]) + "**\n"
            message += "**[" + str(columns[material_column]) + "%]** - "
            if columns[5] != '':
                message += _("Distance from 32 MU : **{distanceFromBubble} ly** - ").format(distanceFromBubble=str(columns[5]))
            if columns[6] != '':
                message += _("Distance from Pytheas : **{distanceFromColonia} ly** - ").format(distanceFromColonia=str(columns[6]))
            message += _("Distance from the main star : **{distanceFromStar} ls**").format(distanceFromStar=str(columns[7]))

            embed = discord.Embed(title="", description=message, color=0x00ffaa)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Google(bot))
