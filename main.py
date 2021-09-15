import os
import discord
import nextcord
import sqlite3
from dotenv import load_dotenv
from nextcord.ext import commands
import requests
import json

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

# !register ARGUMENTO
@bot.command()
async def register(ctx, arg):

    # Obtiene el ID del autor del mensaje
    member = ctx.message.author

    # Variables Albion Online
    # ID de la guild
    guildID = "w8ofVhjvQWOB3xCczo4szQ"
    # ID de la alianza
    allianceID = "hRqowi9bTw6o44R0bsmIUw"

    # Variables roles Discord
    guildRol = "Member"
    allianceRol = "Officer"

    # ID de los roles
    guildRolID = discord.utils.get(member.guild.roles, name="{}".format(guildRol))
    allianceRolID = discord.utils.get(member.guild.roles, name="{}".format(allianceRol))

    embebInfo = discord.Embed(title="Procesando búsqueda en la guild", color=0xFFA500)
    embebInfo.add_field(name="Buscando a:", value="{}".format(arg), inline=False)
    embebInfo.add_field(name="Tiempo estimado", value="5 minutos", inline=False)
    embebInfo.set_footer(text="Bot creado por: QueenMirna#9103")
    # Mensaje embebido avisando
    await ctx.send(embed=embebInfo)

    # # Petición a la url, y guarda la respuesta
    # API que se usará, con parametrización del usuario
    url = 'https://gameinfo.albiononline.com/api/gameinfo/search?q={}'.format(arg)
    response = requests.get(url)

    # Devuelve la URL y el formato final no es un salto de linea, si no un espacio y se unen dos prints
    # Quedando -> https://gameinfo.albiononline.com/api/gameinfo/search?q=Queenmirna  200
    # print("{}".format(url), end =" ")

    if response.status_code == 200:
        # Transforma la info en texto plano a json
        data_json = json.loads(response.text)
        exist = False

        ## DEBUG
        # # Muestra la info en texto plano
        # print("{}".format(response.text))

        # print(data_json)
        # print(json.dumps(data_json['players'], indent=4))
        ## DEBUG

        # Si players existe en data_json
        if data_json.get('players'):

            for player in data_json['players']:
                
                # INFO - Guild
                # Si player es igual al nombre del jugador pasado devolver datos
                if player['Name'].lower() == arg.lower() and player["GuildId"].lower() == guildID.lower():
                    exist = True

                    # Mensaje embebido
                    embebFindGuild = discord.Embed(title="Jugador encontrado", color=0x00ff00)
                    embebFindGuild.add_field(name="Bievenid@:", value="{}".format(arg), inline=False)
                    embebFindGuild.add_field(name="Rol asignado:", value="{}".format(guildRol), inline=False)
                    embebFindGuild.add_field(name="Nick actualizado a:", value="{}".format(player['Name']), inline=False)
                    embebFindGuild.set_footer(text="Bot creado por: QueenMirna#9103")
                    # Mensaje embebido avisando
                    await ctx.send(embed=embebFindGuild)

                    # Asignar rol
                    await member.add_roles(guildRolID)

                    # Cambiar nombre
                    await member.edit(nick="{}".format(player['Name']))

                    # Falta añádir cambiar el nombre
                    break
                
                # INFO - Alliance
                if player['Name'].lower() == arg.lower() and player["AllianceId"].lower() == allianceID.lower():
                    exist = True
                    # Mensaje embebido
                    embebFindAlliance = discord.Embed(title="Jugador encontrado", color=0x8c004b)
                    embebFindAlliance.add_field(name="Bievenid@:", value="{}".format(arg), inline=False)
                    embebFindAlliance.add_field(name="Rol asignado:", value="{}".format(allianceRol), inline=False)
                    embebFindAlliance.add_field(name="Nick actualizado a:", value="{}".format(player['Name']), inline=False)
                    embebFindAlliance.set_footer(text="Bot creado por: QueenMirna#9103")
                    # Mensaje embebido avisando
                    await ctx.send(embed=embebFindAlliance)

                    # Asignar rol
                    await member.add_roles(allianceRol)

                    # Cambiar nombre
                    await member.edit(nick="{}".format(player['Name']))

                    break

                # Si no existe un jugador con ese nombre, puede que sea incompleto o existan varios, pero no coincide ninguno
                if not exist:
                        # Mensaje embebido
                        embebNotFound = discord.Embed(title="Jugador no encontrado", color=0xFF0000)
                        embebNotFound.add_field(name="El jugador:", value="{}\nSi crees que es un error contacta con un oficial".format(arg), inline=False)
                        embebNotFound.set_footer(text="Bot creado por: QueenMirna#9103")
                        # Mensaje embebido avisando
                        await ctx.send(embed=embebNotFound)
                        break
        
        # No existe ningún jugador con ese nombre, NO devuelve resultados la lista
        else:
            # Mensaje embebido
            embebNotFound = discord.Embed(title="Jugador no encontrado", color=0xFF0000)
            embebNotFound.add_field(name="El jugador:", value="{}\nSi crees que es un error contacta con un oficial".format(arg), inline=False)
            embebNotFound.set_footer(text="Bot creado por: QueenMirna#9103")
            # Mensaje embebido avisando
            await ctx.send(embed=embebNotFound)
    
    # La API no está disponible
    else:
        # Mensaje embebido
        embebFindAlliance = discord.Embed(title="La API no está disponible", color=0xFF0000)
        embebFindAlliance.add_field(name="Error:", value="{}".format(response.status_code), inline=False)
        # Mensaje embebido avisando
        await ctx.send(embed=embebFindAlliance)

# Token del bot a usar
bot.run(TOKEN)
