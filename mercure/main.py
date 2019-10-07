import discord, os, gettext, traceback
from discord.ext import commands
import logging
from logging.handlers import TimedRotatingFileHandler
from config import *
localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locales')
translate = gettext.translation('messages', localedir, languages=[config['LANGUAGE']])
translate.install()
_ = translate.gettext

from data import *
from farm import *


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
async def on_command_error(error, ctx):
    if config['DEBUG']: print(_("on_command_error event"))
    # This prevents any commands with local handlers being handled here in on_command_error.
    if hasattr(ctx.command, 'on_error'):
        return

    # Allows us to check for original exceptions raised and sent to CommandInvokeError.
    # If nothing is found. We keep the exception passed to on_command_error.
    error = getattr(error, 'original', error)

    # Anything in ignored will return and prevent anything happening.
    if isinstance(error, commands.UserInputError):
        return

    # Anything in ignored will return and prevent anything happening.
    elif isinstance(error, commands.CommandNotFound):
        text_help = ""
        text_help += _("- !influence <system> : Display <system>'s factions and their influence/states.\n")
        text_help += _(
            "- !system <system> : Displays every information about a system (coordinates, main state, economy...\n")
        text_help += _("- !traffic <system> : Displays recent traffic information of <system>.\n")
        text_help += _("- !stations <system> : Displays all the stations of <system> with their informations.\n")
        text_help += _("- !farm <material> : Displays systems where material can be found, using CMDR Phoenix's Sheet.\n")
        text_help += _("- !oracle : Display EDSM/EDBB links to consult our factions' state in the Bubble and Colonia.\n")
        text_help += _(
            "- !galnet 01-DEC-3303 : Displays galnet articles of the date entered in shown format. Default is current date.\n")
        text_help += _("- !bigbrother : Display followed factions' influence/state in all the systems they're in.\n")
        text_help += _("- !inara <cmdr name> : Displays the inara profile of that CMDR.\n")
        text_help += _("- !repairs : Shows a list of commodities needed to repair a starport.\n")
        text_help += _("- !ed : Displays Frontier servers' state for Elite Dangerous.\n")
        text_help += _("- !cg : Shows the current active cgs' informations.\n")

        embed = discord.Embed(title=_("Available commands"), description=text_help, color=0x00ff00)
        await ctx.send(embed=embed)

    # All other Errors not returned come here... And we can just print the default TraceBack.
    print(_('Ignoring exception in command {}:').format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


@bot.event
async def on_message(message):
    """Called every time a message is sent on a visible channel.
    This is used to make commands case insensitive.
    Also, we check if we're in the channel where only admins can use the bot
    """
    if config['DEBUG']: print(_("on_message function"))
    await bot.process_commands(message)


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
async def test_farm(ctx, arg):
    if config['DEBUG']: print(_("test_farm command"))
    for site in farm[str(arg).lower()]["sites"][_("bubble")]:
        await ctx.send(site)


@test_farm.error
async def test_farm_error(ctx, error):
    if config['DEBUG']: print(_("test_farm command"))
    message = _("Sorry, but that element is unknown. Here's a list : \n")
    for key in farm.keys():
        message += "- "+str(key).capitalize()+"\n"
    await ctx.send(message)

if __name__ == "__main__":
    try:
        bot.run(config["discord_token"])
    finally:
        exit()
