from discord.ext import commands
import discord
import sqlite3
import os
import asyncio
from dotenv import load_dotenv
from datetime import datetime,timezone
# Load env variables file
load_dotenv()

# Get env var and save to var
TOKEN = os.environ.get("TOKEN")

dbName = os.environ.get("DBNAME")
table_config = os.environ.get("TABLE_CONFIG")
table_register = os.environ.get("TABLE_USER")
table_blacklist = os.environ.get("TABLE_BLACKLIST")

class BlacklistCog(commands.Cog, name="Blacklist Command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="blacklist",
        pass_context=True,
        brief="Blacklist an user on the guild.",
        help="Blacklist Albion Nickname.\nExameple: !blacklist"
    )
    @commands.has_permissions(
                              manage_roles=True
                              )
    async def blacklist(self, ctx):

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
        else:
            return

        reasonOK = False
        
        while not reasonOK:
            await ctx.send("Introduce la razón")

            # This will make sure that the response will only be registered if the following
            # conditions are met:
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
            
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=30)
                reasonOK = True
                reasonResponse = True
            except asyncio.TimeoutError:
                await ctx.send("Terminado tiempo de espera, configuración cancelada")
                reasonOK = True
                reasonResponse = False

        if reasonResponse:
            reason = msg.content
        else:
            return

        con = sqlite3.connect(dbName)

        cur = con.cursor()

        checkUser = cur.execute(f"""SELECT * FROM {table_blacklist} WHERE albionNick='{albionNick}' AND discordGuildIdFK='{DiscordGuildID}'""").fetchall()

        date = datetime.now(timezone.utc).strftime("%d/%m/%Y")
        authorId = ctx.author.mention
        authorNick = ctx.message.author.display_name

        if checkUser == []:
            cur.execute(f"""INSERT INTO {table_blacklist} (
                discordGuildIdFK,
                albionNick,
                reason,
                date,
                authorId,
                authorNick)
                VALUES (?, ?, ?, ?, ?, ?)""", (DiscordGuildID, albionNick, reason, date, authorId, authorNick))
        else:
            
            embebBlacklistInfo = discord.Embed(title="Error", color=0x00ff00)
            embebBlacklistInfo.add_field(name="Ya está en la blacklist", value="{}".format(albionNick), inline=False)
            embebBlacklistInfo.set_footer(text="Bot creado por: QueenMirna#9103")
            # Mensaje embebido avisando
            await ctx.send(embed=embebBlacklistInfo)
        
        con.commit()

        con.close()

        embebBlacklistInfo = discord.Embed(title="Blacklist", color=0x00ff00)
        embebBlacklistInfo.add_field(name="Usuario añadido:", value="{}".format(albionNick), inline=False)
        embebBlacklistInfo.add_field(name="Razón:", value="{}".format(reason), inline=False)
        embebBlacklistInfo.set_footer(text="Bot creado por: QueenMirna#9103")
        # Mensaje embebido avisando
        await ctx.send(embed=embebBlacklistInfo)

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(BlacklistCog(bot))
