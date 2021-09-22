from discord.ext import commands
import discord
import sqlite3

class BlacklistCog(commands.Cog, name="Blacklist Command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="blacklist",
        pass_context=True,
        brief="Blacklist an user on the guild.",
        help="Blacklist Albion Nickname.\nExameple: !blacklist QueenMirna"
    )
    async def blacklist(self, ctx, username):
      print('TODO')

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(BlacklistCog(bot))