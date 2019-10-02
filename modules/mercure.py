import discord
from discord.ext import commands
from main import acces_oracle, is_admin

from config import *
from data import *


class Mercure(commands.Cog):
    def __init__(self, bot):
        if config['DEBUG']: print("Module Mercure chargé")
        self.bot = bot

    def cog_unload(self):
        if config['DEBUG']: print("Module Mercure déchargé")

    @commands.command(pass_context=True)
    async def presence(self, ctx, *, arg):
        await self.bot.change_presence(activity=discord.Game(name=arg))

    @commands.command(pass_context=True, aliases=['aide', 'liste'])
    @acces_oracle()
    async def help(self, ctx):
        if config['DEBUG']: print("Commande aide")
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
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def poke(self, ctx):
        """ Just a poke to be sure the bot is still processing commands """
        if config['DEBUG']: print("Commande poke")
        await ctx.send('Oui oui je suis là...:smiley_cat: ')

    @commands.command(pass_context=True,aliases=['cestquandlamaj', 'cestquandbeyond'])
    @acces_oracle()
    async def maj(self, ctx):
        """ Fun command I did for 2.4 """
        if config['DEBUG']: print("Commande maj")
        await ctx.send("C'est sorti !!!!! :ok_hand: :ok_hand: ")

    @commands.command(pass_context=True)
    @acces_oracle()
    async def reparations(self, ctx):
        """
        Displays the commodities needed to repair a station
        """
        if config['DEBUG']: print("Commande réparation")
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
        await ctx.send(embed=embed)

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
        await ctx.send(embed=embed)

    @commands.command()
    @is_admin()
    async def say(self, ctx, *, arg):
        """
        Allows admins in admin_ids to make the bot talk in #oracle_libre_access
        """
        if config['DEBUG']: print("Commande say")
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

