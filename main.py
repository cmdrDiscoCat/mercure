import discord
from discord.ext import commands
import logging
from logging.handlers import TimedRotatingFileHandler

import os
import traceback

from config import *
from data import *

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
log_filename = os.path.join("logs",'mercure.log')
handler = logging.FileHandler(filename=log_filename, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

fileHandler = TimedRotatingFileHandler('logs/mercure.log', when='midnight')
fileHandler.suffix = "%Y_%m_%d.log"
fileHandler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
fileHandler.setLevel(logging.INFO)
logger.addHandler(fileHandler)

description = '''Assistant BGS de la LGC'''
bot = commands.Bot(command_prefix=config['prefix'], description=description, pm_help=True, heartbeat_timeout=150)
bot.remove_command("help")


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


@bot.event
async def on_ready():
    """
    Actions to do when the bot is connected successfully and ready to process commands
    """
    if config['DEBUG']:
        print('Connecté·e en tant que')
        print(bot.user.name)
        print(bot.user.id)
        print('------')

    # we load all modules
    for f in os.listdir("modules/"):
        if f.endswith('.py'):
            bot.load_extension(f"modules.{f[:-3]}")

    await bot.change_presence(activity=discord.Game(name='aider les cartographes'))


@bot.event
async def on_command(ctx):
    """Called when a command is called. Used to log commands on a file."""
    if config['DEBUG']: print("Event on_command")
    if isinstance(ctx.message.channel, discord.abc.PrivateChannel):
        destination = 'PM'
    else:
        destination = '#{0.channel.name} ({0.guild.name})'.format(ctx.message)
    logger.info('Command by {0} in {1}: {2}'.format(ctx.message.author.display_name, destination, ctx.message.content))


@bot.event
async def on_message(message):
    """Called every time a message is sent on a visible channel.
    This is used to make commands case insensitive.
    Also, we check if we're in the channel where only admins can use the bot
    """
    if config['DEBUG']: print("Fonction on_message")
    await bot.process_commands(message)


@bot.command()
async def load(ctx, ext):
    if config['DEBUG']: print(f"Chargement module {ext}")
    bot.load_extension(f"modules.{ext}")


@bot.command()
async def unload(ctx, ext):
    if config['DEBUG']: print(f"Déchargement module {ext}")
    bot.unload_extension(f"modules.{ext}")


@bot.command()
async def reload(ctx):
    # we reload all modules
    # we load all modules
    for f in os.listdir("modules/"):
        if f.endswith('.py'):
            if config['DEBUG']: print(f"Rechargement module {f[:-3]}")
            bot.unload_extension(f"modules.{f[:-3]}")
            bot.load_extension(f"modules.{f[:-3]}")


@bot.command()
async def test(ctx):
    """ Just a poke to be sure the bot is still processing commands """
    if config['DEBUG']: print("Commande test")
    await ctx.send('Oui oui je suis là...:smiley_cat: ')

if __name__ == "__main__":
    try:
        bot.run(config["discord_token"])
    finally:
        exit()
