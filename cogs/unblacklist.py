from discord.ext import commands
import discord
import sqlite3
import os
import asyncio
from dotenv import load_dotenv
# Load env variables file
load_dotenv()

# Get env var and save to var
TOKEN = os.environ.get("TOKEN")

dbName = os.environ.get("DBNAME")
table_config = os.environ.get("TABLE_CONFIG")
table_register = os.environ.get("TABLE_USER")
table_blacklist = os.environ.get("TABLE_BLACKLIST")

class UnBlacklistCog(commands.Cog, name="Unblacklist Command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="unblacklist",
        pass_context=True,
        brief="Unblacklist an user on the guild.",
        help="Unblacklist Albion Nickname.\nExameple: !Unblacklist"
    )
    @commands.has_permissions(
                              manage_roles=True
                              )
    async def unblacklist(self, ctx):

        DiscordGuildID = ctx.message.guild.id

        albionNickOk = False
        
        while not albionNickOk:
            await ctx.send("Introduce el nick del jugador")

            # This will make sure that the response will only be registered if the following
            # conditions are met:
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
            
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=30)
                albionNickOk = True
                botPrefixResponse = True
            except asyncio.TimeoutError:
                await ctx.send("Terminado tiempo de espera, configuración cancelada")
                albionNickOk = True
                botPrefixResponse = False

        if botPrefixResponse:
            albionNick = msg.content
            albionNickLower = albionNick.lower()
        else:
            return

        con = sqlite3.connect(dbName)

        cur = con.cursor()

        checkUser = cur.execute(f"""SELECT * FROM {table_blacklist} WHERE albionNick='{albionNickLower}' AND discordGuildIdFK='{DiscordGuildID}'""").fetchall()

        if checkUser == []:
            embebBlacklistInfo = discord.Embed(title="Error", color=0xFF0000)
            embebBlacklistInfo.add_field(name="Usuario no encontrado:", value="{}".format(albionNickLower), inline=False)
            embebBlacklistInfo.set_footer(text="Bot creado por: QueenMirna#9103")
            # Mensaje embebido avisando
            await ctx.send(embed=embebBlacklistInfo)

            con.close()

            return
        else:
            cur.execute(f"""DELETE FROM {table_blacklist} 
                WHERE albionNick='{albionNickLower}' AND discordGuildIdFK='{DiscordGuildID}'""")
        
        con.commit()

        con.close()

        embebBlacklistInfo = discord.Embed(title="Blacklist", color=0x00ff00)
        embebBlacklistInfo.add_field(name="Usuario eliminado:", value="{}".format(albionNick), inline=False)
        embebBlacklistInfo.set_footer(text="Bot creado por: QueenMirna#9103")
        # Mensaje embebido avisando
        await ctx.send(embed=embebBlacklistInfo)

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(UnBlacklistCog(bot))
