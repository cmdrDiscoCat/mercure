import discord, os, gettext
from discord.ext import commands
import logging
from logging.handlers import TimedRotatingFileHandler

from config import *
from data import *

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locales')
translate = gettext.translation('messages', localedir, languages=[config['LANGUAGE']])
translate.install()
_ = translate.gettext


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
log_filename = os.path.join("..","logs",'mercure.log')
handler = logging.FileHandler(filename=log_filename, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

fileHandler = TimedRotatingFileHandler(os.path.join("..","logs",'mercure.log'), when='midnight')
fileHandler.suffix = "%Y_%m_%d.log"
fileHandler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
fileHandler.setLevel(logging.INFO)
logger.addHandler(fileHandler)

description = _('''LGC's BGS assistant''')
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
        if str(ctx.message.channel) == channel_for_daily_post_name:
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
        print(_("Logged in as"))
        print(bot.user.name)
        print(bot.user.id)
        print('------')

    # we load all modules
    for f in os.listdir("modules"+os.sep):
        if f.endswith('.py'):
            bot.load_extension(f"modules.{f[:-3]}")

    await bot.change_presence(activity=discord.Game(name=_('helping the cartographers')))


@bot.event
async def on_command(ctx):
    """Called when a command is called. Used to log commands on a file."""
    if config['DEBUG']: print(_("on_command event"))
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
    if config['DEBUG']: print(_("on_message function"))
    await bot.process_commands(message)


@bot.command()
async def load(ctx, ext):
    if config['DEBUG']: print(_("Module {module} loaded").format(module=ext))
    bot.load_extension(f"modules.{ext}")


@bot.command()
async def unload(ctx, ext):
    if config['DEBUG']: print(_("Module {module} unloaded").format(module=ext))
    bot.unload_extension(f"modules.{ext}")


@bot.command()
async def reload(ctx):
    # we reload all modules
    # we load all modules
    for f in os.listdir("modules"+os.sep):
        if f.endswith('.py'):
            if config['DEBUG']: print(_("Module {module} reloaded").format(module=f[:-3]))
            bot.unload_extension(f"modules.{f[:-3]}")
            bot.load_extension(f"modules.{f[:-3]}")


@bot.command()
async def test(ctx):
    """ Just a poke to be sure the bot is still processing commands """
    if config['DEBUG']: print(_("test command"))
    await ctx.send(_("Yeah yeah i'm here...:smiley_cat: "))

if __name__ == "__main__":
    try:
        bot.run(config["discord_token"])
    finally:
        exit()
