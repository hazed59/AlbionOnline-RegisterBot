from discord.ext import commands
import discord
from datetime import datetime,timezone

class utcCog(commands.Cog, name="utc Command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context=True,
        brief="Get UTC time",
        help="Get UTC time.\nExameple: !utc",
    )
    async def utc(self, ctx):

        now_utc = datetime.now(timezone.utc).strftime("%H:%M:%S")

        utcTime = discord.Embed(description="⏰ UTC time now: {}".format(now_utc))

        await ctx.send(embed=utcTime)

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(utcCog(bot))