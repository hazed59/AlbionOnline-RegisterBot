import os
# Discord lib
import discord
# Netxcord (discordpy) lib
import nextcord
# Sqlite lib
import sqlite3
# Load .env file lib
from dotenv import load_dotenv
# Carga TODOS (*) los .py de la carpeta comandos
from comandos import *
# Framework de python para comandos
from nextcord.ext import commands

# Load env variables file
load_dotenv()

# Get env var and save to var
TOKEN = os.environ.get("TOKEN")

# Prefijo de los comandos
bot = commands.Bot(command_prefix='!')

# Iniciar bot con el token introducido
@bot.event
async def on_ready():
    # Mensaje mostrando que está iniciado
    print('Logged in as {0.user}'.format(bot))

# Token del bot a usar
bot.run(TOKEN)
