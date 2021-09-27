import discord
from discord.ext import commands
import sqlite3
from nextcord.ext.commands.context import P
import os
from dotenv import load_dotenv

load_dotenv()

dbName = os.environ.get("DBNAME")
table_config = os.environ.get("TABLE_CONFIG")
table_register = os.environ.get("TABLE_USER")
table_blacklist = os.environ.get("TABLE_BLACKLIST")
class checkCog(commands.Cog, name="checkbl Command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context=True,
        brief="Get user info",
        help="Get user blacklist info (blacklist reason, date, and user who blacklist him).\nExameple: !checkbl QueenMirna",
    )
    async def checkbl(self, ctx, nick):

        DiscordGuildID = ctx.message.guild.id
        username = nick.lower()

        con = sqlite3.connect('{}'.format(dbName))

        cur = con.cursor()

        try:
            checkReason = cur.execute(f"""SELECT reason FROM {table_blacklist} WHERE discordGuildIdFK='{DiscordGuildID}' AND albionNick='{username}'""").fetchall()[0][0]
            checkDate = cur.execute(f"""SELECT date FROM {table_blacklist} WHERE discordGuildIdFK='{DiscordGuildID}' AND albionNick='{username}'""").fetchall()[0][0]
            checkMention = cur.execute(f"""SELECT authorId FROM {table_blacklist} WHERE discordGuildIdFK='{DiscordGuildID}' AND albionNick='{username}'""").fetchall()[0][0]
            checkAuthorNick = cur.execute(f"""SELECT authorNick FROM {table_blacklist} WHERE discordGuildIdFK='{DiscordGuildID}' AND albionNick='{username}'""").fetchall()[0][0]
            con.close()
        except (sqlite3.OperationalError, IndexError):
            await ctx.send("El usuario no está en la blacklist.")
            con.close()
            return

        embebCheckGuild = discord.Embed(title="Blacklist", color=0xFFA500)
        embebCheckGuild.add_field(name="Usuario", value="{}".format(username), inline=True)
        embebCheckGuild.add_field(name="Fecha", value="{}".format(checkDate), inline=True)
        embebCheckGuild.add_field(name="Razón", value="{}".format(checkReason), inline=False)
        embebCheckGuild.add_field(name="Blacklisteado por", value="{} - {}".format(checkAuthorNick, checkMention), inline=True)
        embebCheckGuild.set_footer(text="Bot creado por: QueenMirna#9103")
        # Mensaje embebido avisando
        await ctx.send(embed=embebCheckGuild)

    @checkbl.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embebCheckError = discord.Embed(title="Error", color=0xFF0000)
            embebCheckError.add_field(name="Info:", value="Introduce un nombre de usuario", inline=False)
            embebCheckError.set_footer(text="Bot creado por: QueenMirna#9103")
            # Mensaje embebido avisando
            await ctx.send(embed=embebCheckError)
# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(checkCog(bot))