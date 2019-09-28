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
log_filename = os.path.join("logs",'hermes.log')
handler = logging.FileHandler(filename=log_filename, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

fileHandler = TimedRotatingFileHandler('logs/discobot.log', when='midnight')
fileHandler.suffix = "%Y_%m_%d.log"
fileHandler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
fileHandler.setLevel(logging.INFO)
logger.addHandler(fileHandler)

description = '''Assistant BGS de la LGC'''
bot = commands.Bot(command_prefix=config['prefix'], description=description, pm_help=True, heartbeat_timeout=150)
bot.remove_command("help")


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


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

@bot.event
def on_ready():
    """
    Actions to do when the bot is connected successfully and ready to process commands
    """
    print('Connecté·e en tant que')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    # we load all modules
    for f in os.listdir("modules/"):
        if f.endswith('.py'):
            client.load_extension(f"modules.{f[:-3]}")

    yield from bot.change_presence(game=discord.Game(name='aider les cartographes'))


@bot.event
def on_command(command, ctx):
    """Called when a command is called. Used to log commands on a file."""
    if ctx.message.channel.is_private:
        destination = 'PM'
    else:
        destination = '#{0.channel.name} ({0.server.name})'.format(ctx.message)
    logger.info('Command by {0} in {1}: {2}'.format(ctx.message.author.display_name, destination, ctx.message.content))


@bot.event
def on_command_error(error, ctx):
    """
    What we do when there's something going wrong
    - Unknown command
    - Invoke error
    - Something else
    """
    if isinstance(error, commands.errors.CommandNotFound):
        aide_texte = "- !influence Nom du système : Affiche l'influence des factions d'un système.\n"\
        "- !systeme Nom du système : Affiche les informations (coordonnées, gouvernement, sécurité, économie...) d'un système.\n"\
        "- !trafic Nom du système : Affiche les informations sur le trafic récent d'un système.\n"\
        "- !stations Nom du système : Affiche les stations (avec leurs informations) d'un système.\n"\
        "- !farm Nom de matériau : Affiche les systèmes du tableau du Capitaine Phoenix où l'élément demandé peut être trouvé.\n"\
        "- !oracle : Affiche la liste des liens EDSM et EDDB pour aller y consulter l'état de la LGC dans la bulle et à Colonia.\n"\
        "- !galnet 01-DEC-3303 : Affiche les articles galnet de ce jour, remplacez 01-DEC-3303 par la date qui vous intéresse. Par défaut c'est à la date du jour.\n"\
        "- !bigbrother : Affiche la liste des systèmes où LGC est présent dans la bulle et à Colonia, ainsi que notre influence dans chacun de ces systèmes.\n"\
        "- !inara \"Nom de pilote\" : Affiche le profil de pilote Inara correspondant au nom demandé.\n"\
        "- !reparations : Affiche les commodités nécessaires en français et en anglais pour réparer les stations.\n"\
        "- !ed : Affiche l'état des serveurs Frontier pour Elite Dangerous.\n"\
        "- !cg : Affiche la liste et les infos des CG en cours.\n"
        embed = discord.Embed(title="Liste des commandes disponibles", description=aide_texte, color=0x00ff00)
        yield from bot.send_message(ctx.message.channel, embed=embed)
    elif isinstance(error, commands.CommandInvokeError):
        print('In {0.command.qualified_name}:'.format(ctx))
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original))
    else:
        return


@bot.event
def on_message(message):
    """Called every time a message is sent on a visible channel.
    This is used to make commands case insensitive.
    Also, we check if we're in the channel where only admins can use the bot
    """
    yield from bot.process_commands(message)


@bot.command()
async def load(ctx, ext):
    bot.load_extension(f"modules.{ext}")


@bot.command()
async def unload(ctx, ext):
    bot.unload_extension(f"modules.{ext}")


@bot.command()
async def reload(ctx, ext):
    bot.unload_extension(f"modules.{ext}")
    bot.load_extension(f"modules.{ext}")


if __name__ == "__main__":
    try:
        bot.run(config["discord_token"])
    finally:
        exit()
