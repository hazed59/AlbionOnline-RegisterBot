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

dbName = os.environ.get("DBNAME")
table_config = os.environ.get("TABLE_CONFIG")
table_register = os.environ.get("TABLE_USER")
table_blacklist = os.environ.get("TABLE_BLACKLIST")

def botPrefixes(bot, message):

    if (message.guild is None):
        return "!"
    else:
        table_config = "DiscordServersConfig"

        DiscordGuildID = message.guild.id

        con = sqlite3.connect('{}'.format(dbName))

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
    con = sqlite3.connect('{}'.format(dbName))

    # Create cursor
    cur = con.cursor()

    # Se pone "f" delante para que se reconozca las {} como variables
    # Crear tabla de la configuración de la guild
    cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_config} 
                (discordGuildId INTEGER PRIMARY KEY,
                botPrefix TEXT,
                guildId TEXT,
                guildTag TEXT,
                guildRol TEXT,
                allianceId TEXT,
                allianceTag TEXT,
                allianceRol TEXT)"""
                )
    
    cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_register} 
            (userId INTEGER PRIMARY KEY,
            discordGuildIdFK INTEGER,
            albionNick TEXT,
            FOREIGN KEY (discordGuildIdFK) REFERENCES {table_config} (discordGuildId)
            )"""
            )

    cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_blacklist} 
            (discordGuildIdFK INTEGER,
            albionNick TEXT,
            reason TEXT,
            date TEXT,
            authorId INT,
            authorNick TEXT,
            FOREIGN KEY (discordGuildIdFK) REFERENCES {table_config} (discordGuildId)
            )"""
            )
    
    con.commit()

    # Cerrar conexión
    con.close()

    print('Logged in as {0.user}'.format(bot))

@bot.event
async def on_guild_remove(guild):

    DiscordGuildID = guild.id

    con = sqlite3.connect('{}'.format(dbName))

    cur = con.cursor()

    cur.execute(f"""DELETE FROM {table_config} where discordGuildId={DiscordGuildID}""")

    cur.execute(f"""DROP FROM {table_register} where discordGuildIdFK={DiscordGuildID}""")
             
    # Guardar cambios
    con.commit()

    con.close()

# Below cogs represents our folder our cogs are in. Following is the file name. So 'setup.py' in cogs, would be cogs.setup
# Think of it like a dot path import
initial_extensions = [
                    'cogs.setup',
                    'cogs.register',
                    'cogs.unregister',
                    'cogs.blacklist',
                    'cogs.unblacklist',
                    'cogs.utc',
                    'cogs.check'
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
