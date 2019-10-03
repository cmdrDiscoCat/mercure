import discord
from discord.ext import commands
from main import acces_oracle, is_admin

from config import *
from data import *

import gettext

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locales')
translate = gettext.translation('mercure', localedir, languages=[config['LANGUAGE']], fallback=True)
_ = translate.gettext


class Mercure(commands.Cog):
    def __init__(self, bot):
        if config['DEBUG']: print(_("Mercure module loaded"))
        self.bot = bot

    def cog_unload(self):
        if config['DEBUG']: print(_("Mercure module unloaded"))

    @commands.command(pass_context=True)
    async def presence(self, ctx, *, arg):
        await self.bot.change_presence(activity=discord.Game(name=arg))

    @commands.command(pass_context=True, aliases=['aide', 'liste'])
    @acces_oracle()
    async def help(self, ctx):
        if config['DEBUG']: print(_("help command"))
        text_help = ""
        text_help += _("- !influence <system> : Display <system>'s faction and their influence/states.\n")
        text_help += _("- !system <system> : Displays every information about a system (coordinates, main state, economy...\n")
        text_help += _("- !traffic <system> : Displays recent traffic information of <system>.\n")
        text_help += _("- !stations <system> : Displays all the stations of <system> with their informations.\n")
        text_help += _("- !farm <material> : Displays systems where material can be found, using CMDR Phoenix's Sheet.\n")
        text_help += _("- !oracle : Display EDSM/EDBB links to consult our factions' state in the Bubble and Colonia.\n")
        text_help += _("- !galnet 01-DEC-3303 : Displays galnet articles of the date entered in shown format. Default is current date.\n")
        text_help += _("- !bigbrother : Display followed factions' influence/state in all the systems they're in.\n")
        text_help += _("- !inara <cmdr name> : Displays the inara profile of that CMDR.\n")
        text_help += _("- !reparations : Shows a list of commodities needed to repair a starport.\n")
        text_help += _("- !ed : Displays Frontier servers' state for Elite Dangerous.\n")
        text_help += _("- !cg : Shows the current active cgs' informations.\n")

        embed = discord.Embed(title=_("Available commands"), description=text_help, color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def poke(self, ctx):
        """ Just a poke to be sure the bot is still processing commands """
        if config['DEBUG']: print(_("poke command"))
        await ctx.send(_("Yeah yeah i'm here...:smiley_cat: "))

    @commands.command(pass_context=True,
                      aliases=['update', 'cestquandlamaj', 'cestquandbeyond', 'whenisitout', 'whenisbeyondout'])
    @acces_oracle()
    async def maj(self, ctx):
        """ Fun command I did for 2.4 """
        if config['DEBUG']: print(_("maj command"))
        await ctx.send(_("It's out !!!!! :ok_hand: :ok_hand: "))

    @commands.command(pass_context=True)
    @acces_oracle()
    async def reparations(self, ctx):
        """
        Displays the commodities needed to repair a station
        """
        if config['DEBUG']: print(_("repairs command"))
        desc = ""
        desc += _("- Indium \n")
        desc += _("- Gallium \n")
        desc += _("- Titanium \n")
        desc += _("- Copper \n")
        desc += _("- Aluminium \n")
        desc += _("- Synthetic Fabrics \n")
        desc += _("- Polymers \n")
        desc += _("- Water Purifiers \n")
        desc += _("- Robotics \n")
        desc += _("- Ceramic composites \n")
        desc += _("- CMM composites \n")
        desc += _("- Insulating Membrane \n")
        desc += _("- Power Converters \n")
        desc += _("- Natural Fabrics \n")
        "
        embed = discord.Embed(title=_("Commodities needed to repair a starport"),
                              description=desc, color=0x00ffaa)
        await ctx.send(embed=embed)

    @commands.command()
    @is_admin()
    async def say(self, ctx, *, arg):
        """
        Allows admins in admin_ids to make the bot talk in #oracle_libre_access
        """
        if config['DEBUG']: print(_("say command"))
        channel = self.bot.get_channel(385734721402961920)
        await ctx.send(channel, arg)

    @commands.command()
    @acces_oracle()
    async def lgc(self):
        pass

    @commands.command()
    @acces_oracle()
    async def conditions(self):
        pass


def setup(bot):
    bot.add_cog(Mercure(bot))

