from discord.ext import commands
import sqlite3
import discord
import os
from dotenv import load_dotenv

load_dotenv()

dbName = os.environ.get("DBNAME")
table_config = os.environ.get("TABLE_CONFIG")
table_register = os.environ.get("TABLE_USER")
table_blacklist = os.environ.get("TABLE_BLACKLIST")

class UnregisterCog(commands.Cog, name="Unregister Command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context=True,
        brief="Unregister user on the guild.",
        help="Unregister user on the guild.\nExameple: !unregister",
    )

    async def unregister(self, ctx):

        memberId = ctx.message.author.id
        con = sqlite3.connect(dbName)

        cur = con.cursor()

        DiscordGuildID = ctx.message.guild.id

        checkUser = cur.execute(f"""SELECT userid FROM {table_register} WHERE userid='{memberId}' AND discordGuildIdFK='{DiscordGuildID}'""").fetchall()

        if len(checkUser) > 0:

            checkNick = cur.execute(f"""SELECT albionnick FROM {table_register} WHERE userid='{memberId}' AND discordGuildIdFK='{DiscordGuildID}'""").fetchall()[0][0]

            cur.execute(f"""DELETE FROM {table_register} WHERE userid='{memberId}' AND discordGuildIdFK='{DiscordGuildID}'""")

            embebInfo = discord.Embed(title="Registro eliminado", color=0xff0000)
            embebInfo.add_field(name="Eliminado tu nick asociado", value="{}".format(checkNick), inline=False)
            embebInfo.set_footer(text="Bot creado por: QueenMirna#9103")

            # Mensaje embebido avisando
            await ctx.send(embed=embebInfo)

            con.commit()

            con.close()

            return

        else:
            con.close()

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(UnregisterCog(bot))