import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import sqlite3
import asyncio

# Load env variables file
load_dotenv()

dbName = os.environ.get("DBNAME")
table_register = os.environ.get("TABLE_USER")

class clearRegisterCog(commands.Cog, name="clearregister Command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context=True,
        brief="Clear users data",
        help="Clear user registration.\nExameple: !clearregister",
    )
    async def utc(self, guild, ctx):

        clearRegisterConfirm = discord.Embed(description="¿Estás seguro que quieres eliminar los registros (lista negra y registros)? Y/N")

        await ctx.send(embed=clearRegisterConfirm)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and \
            msg.content.lower() in ["y", "n"]

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=30)
            if msg.content.lower() == "y":

                DiscordGuildID = guild.id

                con = sqlite3.connect('{}'.format(dbName))

                cur = con.cursor()

                cur.execute(f"""DELETE FROM {table_register} where discordGuildIdFK={DiscordGuildID}""")

                # Guardar cambios
                con.commit()

                con.close()

                clearRegister = discord.Embed(description="Registros de usuarios eliminados del sistema")

                await ctx.send(embed=clearRegister)
            
            else:

                await ctx.send("Eliminación de registros del sistema cancelado")

        except asyncio.TimeoutError:
            await ctx.send("Terminado tiempo de espera, configuración cancelada")
            guildExist = True
            guildResponse = False

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(clearRegisterCog(bot))
