import discord
from discord.ext import commands

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

class Mercure(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['aide', 'liste'])
    @acces_oracle()
    async def help(self, ctx):
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
        await ctx.send_message(ctx.message.channel, embed=embed)


    @commands.command(pass_context=True)
    @acces_oracle()
    async def poke(self, ctx):
        """ Just a poke to be sure the bot is still processing commands """
        await ctx.send_message(ctx.message.channel, 'Oui oui je suis là...:smiley_cat: ')


    @commands.command(pass_context=True,aliases=['cestquandlamaj', 'cestquandbeyond'])
    @acces_oracle()
    async def maj(self, ctx):
        """ Just a poke to be sure the bot is still processing commands """
        await ctx.send_message(ctx.message.channel, "C'est sorti !!!!! :ok_hand: :ok_hand: ")


    @commands.command(pass_context=True)
    @acces_oracle()
    async def reparations(self, ctx):
        """
        Displays the commodities needed to repair a station
        """
        desc = ""
        desc += "- Indium \n" \
                "- Gallium \n" \
                "- Titanium \n" \
                "- Cuivre \n" \
                "- Aluminium \n" \
                "- Tissus synthétiques \n" \
                "- Polymères \n" \
                "- Purificateurs d'eau \n" \
                "- Robots \n" \
                "- Composés céramiques \n" \
                "- Composés CCM \n" \
                "- Membrane isolante \n" \
                "- Convertisseur d'énergie \n" \
                "- Tissus naturels \n"

        embed = discord.Embed(title="Liste des commodités nécessaires à la réparation d'une station", description=desc,
                              color=0xaaffaa)
        await ctx.send_message(ctx.message.channel, embed=embed)

        desc_en = ""
        desc_en += "- Indium \n" \
                   "- Gallium \n" \
                   "- Titanium \n" \
                   "- Copper \n" \
                   "- Aluminium \n" \
                   "- Synthetic Fabrics \n" \
                   "- Polymers \n" \
                   "- Water Purifiers \n" \
                   "- Robotics \n" \
                   "- Ceramic composites \n" \
                   "- CMM composites \n" \
                   "- Insulating Membrane \n" \
                   "- Power Converters \n" \
                   "- Natural Fabrics \n"

        embed = discord.Embed(title="Commodities needed to repair a starport",
                              description=desc_en, color=0x00ffaa)
        await ctx.send_message(ctx.message.channel, embed=embed)

    @commands.command()
    @is_admin()
    async def say(self, ctx, *, arg):
        """
        Allows admins in admin_ids to make the bot talk in #oracle_libre_access
        """
        channel = self.bot.get_channel('385734721402961920')
        await ctx.send_message(channel, arg)

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

