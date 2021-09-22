import os
import discord
import sqlite3
from dotenv import load_dotenv
from nextcord.ext import commands
import sys, traceback

# Load env variables file
load_dotenv()

# Get env var and save to var
TOKEN = os.environ.get("TOKEN")

def botPrefixes(bot, message):

    if (message.guild is None):
        return "!"
    else:
        table_config = "DiscordServersConfig"

        DiscordGuildID = message.guild.id

        con = sqlite3.connect('example.db')

        cur = con.cursor()

        try:
            botPrefix = cur.execute(f"""SELECT botPrefix FROM {table_config} where discordGuildId={DiscordGuildID}""").fetchall()[0]
        except (sqlite3.OperationalError, IndexError):
            return "!"
        
        con.close()

        return botPrefix[0]

bot = commands.Bot(
    command_prefix= (botPrefixes)
    )

# Ignore DMs
@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None

# Iniciar bot con el token introducido
@bot.event
async def on_ready():
    # Mensaje mostrando que está iniciado
    print('Logged in as {0.user}'.format(bot))

@bot.event
async def on_guild_remove(guild):

    table_config = "DiscordServersConfig"

    DiscordGuildID = guild.id

    table_users = "registeredUsers{}".format(DiscordGuildID)

    con = sqlite3.connect('example.db')

    cur = con.cursor()

    cur.execute(f"""DELETE FROM {table_config} where discordGuildId={DiscordGuildID}""")

    cur.execute(f"""DROP TABLE {table_users}""")
             
    # Guardar cambios
    con.commit()

    con.close()

@bot.command(
    pass_context=True,
    brief="Unregister user on the guild.",
    help="Unregister user on the guild.\nExameple: !unregister"
)
async def unregister(ctx):

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

# Below cogs represents our folder our cogs are in. Following is the file name. So 'setup.py' in cogs, would be cogs.setup
# Think of it like a dot path import
initial_extensions = [
                    'cogs.setup',
                    'cogs.register'
                    ]

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

# Help command in embeb
class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

bot.help_command = MyHelpCommand()

# Token del bot a usar
bot.run(TOKEN, reconnect=True)
