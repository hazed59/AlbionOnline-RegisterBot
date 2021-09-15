import requests
import json
import os
import discord
import nextcord

# Framework de python para comandos
from nextcord.ext import commands
bot = commands.Bot(command_prefix='!')

# Iniciar bot con el token introducido
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

# !register ARGUMENTO
@bot.command()
async def register(ctx, arg):

    # Obtiene el ID del autor del mensaje
    member = ctx.message.author

    # Variables Albion Online
    # ID de la guild
    guildID = "XXXXXX"
    # ID de la alianza
    allianceID = "XXXXXX"

    # ID de los roles
    guildRolID = discord.utils.get(member.guild.roles, name="Member")
    allianceRolID = ""

    await ctx.send("Buscando a {} en la guild, esto puede tardar hasta 5 minutos, se paciente.".format(arg))
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
            
                # Si player es igual al nombre del jugador pasado devolver datos
                if player['Name'].lower() == arg.lower() and player["GuildId"].lower() == guildID.lower():
                    exist = True
                    await ctx.send("Has sido encontrado en el gremio {}, se te acaba de asignar el rol, bienvenido al gremio ".format(player["GuildName"]))
                    await member.add_roles(guildRolID)
                    # Falta añádir que le de el rol y le cambie el nombre
                    # Añadir que le rol o nombre si es clan o alianza
                    break

                if player['Name'].lower() == arg.lower() and player["AllianceId"].lower() == allianceID.lower():
                    exist = True
                    await ctx.send("{}".format(player["AllianceName"]))
                    # Falta añádir que le de el rol y le cambie el nombre
                    # Añadir que le rol o nombre si es clan o alianza
                    break

                # Si no existe un jugador con ese nombre, puede que sea incompleto o existan varios, pero no coincide ninguno
                if not exist:
                        await ctx.send("No existe el jugador {}, verifica que el nombre sea igual que en el juego.".format(arg))
        
        # No existe ningún jugador con ese nombre, NO devuelve resultados la lista
        else:
            await ctx.send("No existe el jugador {}, verifica que el nombre sea igual que en el juego, incluyendo mayúsculas y minúsculas.".format(arg))
    
    # La API no está disponible
    else:
        await ctx.send("La API no está disponible por el siguiente error: {}".format(response.status_code))

# Token del bot a usar
bot.run('XXXXXXXXX')