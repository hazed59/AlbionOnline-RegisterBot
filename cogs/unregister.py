from discord.ext import commands
import sqlite3
import discord

class UnregisterCog(commands.Cog, name="Unregister Command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context=True,
        brief="Unregister user on the guild.",
        help="Unregister user on the guild.\nExameple: !unregister",
        cog_name="Register Commands"
    )
    async def unregister(self, ctx):

        memberId = ctx.message.author.id
        con = sqlite3.connect('example.db')

        cur = con.cursor()

        DiscordGuildID = ctx.message.guild.id
        table_users = "registeredUsers{}".format(DiscordGuildID)

        checkUser = cur.execute(f"""SELECT userid FROM {table_users} where userid={memberId}""").fetchall()

        if len(checkUser) > 0:

            checkNick = cur.execute(f"""SELECT albionnick FROM {table_users}""").fetchall()[0][0]

            cur.execute(f"""DELETE FROM {table_users} where userid={memberId}""")

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