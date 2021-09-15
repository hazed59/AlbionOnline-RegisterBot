import requests
import json
import os
import discord
# Framework de python para comandos
from discord.ext import commands
bot = commands.Bot(command_prefix='!')

# API que se usará, con parametrización del usuario
url = 'https://gameinfo.albiononline.com/api/gameinfo/search?q={}'.format(arg)

client = discord.Client()

# Iniciar bot con el token introducido
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Token del bot a usar
client.run('your token here')

# !register ARGUMENTO
@bot.command()
async def register(ctx, arg):
    # await ctx.send(arg)
    # Petición a la url, y guarda la respuesta
    response = requests.get(url)

    # Devuelve la URL y el formato final no es un salto de linea, si no un espacio y se unen dos prints
    # Quedando -> https://gameinfo.albiononline.com/api/gameinfo/search?q=Queenmirna  200
    # print("{}".format(url), end =" ")

    if response.status_code == 200:
        # Transforma la info en texto plano a json
        data_json = json.loads(response.text)
        exist = False

        # Si players existe en data_json
        if data_json.get('players'):

            for player in data_json['players']:
            
                # Si player es igual al nombre del jugador pasado devolver datos
                if player['Name'].lower() == arg.lower():
                    exist = True
                    # Falta añádir que le de el rol y le cambie el nombre
                    # Añadir que le rol o nombre si es clan o alianza

            # Si no existe un jugador con ese nombre, puede que sea incompleto o existan varios, pero no coincide ninguno
            if not exist:
                    ctx.send("No existe el jugador {}, verifica que el nombre sea igual que en el juego.".format(arg))
        
        # No existe ningún jugador con ese nombre, NO devuelve resultados la lista
        else:
            ctx.send("No existe el jugador {}, verifica que el nombre sea igual que en el juego.".format(arg))
    
    # La API no está disponible
    else:
        ctx.send("La API no está disponible por el siguiente error: {}".format(response.status_code))

# Muestra la info en texto plano
# print("{}".format(response.text))


# print(data_json)
# print(json.dumps(data_json['players'], indent=4))
