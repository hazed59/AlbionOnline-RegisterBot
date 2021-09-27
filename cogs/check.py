from discord.ext import commands
import discord
from datetime import datetime,timezone

class checkCog(commands.Cog, name="check Command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context=True,
        brief="Get user info",
        help="Get user info (Guild, ).\nExameple: !check",
    )
    async def check(self, ctx):
      await ctx.send("Hi")

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(checkCog(bot))