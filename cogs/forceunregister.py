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
class forceUnregisterCog(commands.Cog, name="checkbl Command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context=True,
        brief="Force unregister user",
        help="Force unregister user, to fix nickname thieves or double registration.\nExameple: !checkbl QueenMirna",
    )
    @commands.has_permissions(
                              manage_roles=True
                              )
    async def forceUnregister(self, ctx, user):

        username = user.lower()

        DiscordGuildID = ctx.guild.id

        con = sqlite3.connect('{}'.format(dbName))

        cur = con.cursor()

        cur.execute(f"""DELETE FROM {table_blacklist} WHERE discordGuildIdFK='{DiscordGuildID}' AND albionNick='{username}'""")

        # Guardar cambios
        con.commit()

        con.close()

        ctx.send("Usuario **{}** eliminado de la blacklist".format(username))

    @forceUnregister.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embebforceUnregisterError = discord.Embed(title="Error", color=0xFF0000)
            embebforceUnregisterError.add_field(name="Info:", value="Introduce un nombre de usuario", inline=False)
            embebforceUnregisterError.set_footer(text="Bot creado por: QueenMirna#9103")
            # Mensaje embebido avisando
            await ctx.send(embed=embebforceUnregisterError)

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(forceUnregisterCog(bot))