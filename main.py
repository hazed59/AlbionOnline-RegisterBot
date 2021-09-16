import os
import discord
import nextcord
import sqlite3
from dotenv import load_dotenv
from nextcord.ext import commands
import requests
import json
import asyncio

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

@bot.command(
    pass_context=True,
    brief="Initial bot setup.",
    help="Configure bot prefix, Guild ID, Guild TAG, Alliance ID and Alliance TAG."
)
# Check if have admin perms
@commands.has_permissions(administrator=True)
async def setup2(ctx):
    # Guardar la ID de la guild
    DiscordGuildID = ctx.message.guild.id
    # Nombre de las tablas según ID de la guild
    table_users = "{}user".format(DiscordGuildID)
    table_config = "{}config".format(DiscordGuildID)

    botPrefixOk = False
    while not botPrefixOk:
        await ctx.send("Introduce el prefijo del bot")

        # This will make sure that the response will only be registered if the following
        # conditions are met:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        try:
            msg = await bot.wait_for("message", check=check, timeout=5)
            botPrefixOk = True
            botPrefixResponse = True
        except asyncio.TimeoutError:
            await ctx.send("Terminado tiempo de espera, configuración cancelada")
            botPrefixOk = True
            botPrefixResponse = False

    if botPrefixResponse:
        botPrefix = msg.content
    else:
        return

    guildExist = False
    while not guildExist:
        await ctx.send("Introduce la ID del gremio")

        # This will make sure that the response will only be registered if the following
        # conditions are met:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            msg = await bot.wait_for("message", check=check, timeout=5)
            guildResponse = True
        except asyncio.TimeoutError:
            await ctx.send("Terminado tiempo de espera, configuración cancelada")
            guildExist = True
            guildResponse = False

        if guildResponse:
            guildId = msg.content

            guildUrl = 'https://gameinfo.albiononline.com/api/gameinfo/guilds/{}'.format(guildId)
            guildResponse = requests.get(guildUrl)

            if guildResponse.status_code == 200:
                guild_data_json = json.loads(guildResponse.text)
                # Mensaje embebido
                embebCheckGuild = discord.Embed(title="Comprobación", color=0xFFA500)
                embebCheckGuild.add_field(name="Info", value="Tu guild se llama: **{}**".format(guild_data_json['Name']), inline=False)
                embebCheckGuild.add_field(name="¿Es correcto?", value="Si es así, escribe **Y**, para continuar, sino **N** para introducir uno nuevo")
                embebCheckGuild.set_footer(text="Bot creado por: QueenMirna#9103")
                # Mensaje embebido avisando
                await ctx.send(embed=embebCheckGuild)
                # This will make sure that the response will only be registered if the following
                # conditions are met:
                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel and \
                    msg.content.lower() in ["y", "n"]

                try:
                    msg = await bot.wait_for("message", check=check, timeout=5)
                    if msg.content.lower() == "y":
                        await ctx.send("ZI")
                        guildExist = True
                        guildResponse = True

                except asyncio.TimeoutError:
                    await ctx.send("Terminado tiempo de espera, configuración cancelada")
                    guildExist = True
                    guildResponse = False
            else:
                # Mensaje embebido
                embebErrorGuild = discord.Embed(title="ID de guild no encontrado", color=0xFF0000)
                embebErrorGuild.add_field(name="Info:", value="Comprueba que el ID de la guild es: {}".format(guildId), inline=False)
                embebErrorGuild.set_footer(text="Bot creado por: QueenMirna#9103")
                # Mensaje embebido avisando
                await ctx.send(embed=embebErrorGuild)

    if guildExist:
        botPrefixOk = True
    else:
        return

        # if guildExist:
        #     await ctx.send("Introduce el TAG del gremio")

        #     # This will make sure that the response will only be registered if the following
        #     # conditions are met:
        #     def check(msg):
        #         return msg.author == ctx.author and msg.channel == ctx.channel

        #     try:
        #         msg = await bot.wait_for("message", check=check, timeout=30)
        #     except asyncio.TimeoutError:
        #         await ctx.send("Terminado tiempo de espera, configuración cancelada")

        #     guildTag = msg.content

        # if guildExist:
        #     allianceExist = False
        #     while not allianceExist:
        #         await ctx.send("Introduce la ID de la alianza")

        #         # This will make sure that the response will only be registered if the following
        #         # conditions are met:
        #         def check(msg):
        #             return msg.author == ctx.author and msg.channel == ctx.channel

        #         try:
        #             msg = await bot.wait_for("message", check=check, timeout=30)
        #         except asyncio.TimeoutError:
        #             await ctx.send("Terminado tiempo de espera, configuración cancelada")
        #             allianceExist = True

        #     allianceId = msg.content

        #     allianceUrl = 'https://gameinfo.albiononline.com/api/gameinfo/alliances/{}'.format(allianceId)
        #     guildResponse = requests.get(allianceUrl)

        #     if guildResponse.status_code == 200:
        #         guild_data_json = json.loads(guildResponse.text)
        #         guildExist = True
        #     else:
        #         # Mensaje embebido
        #         embebErrorAlliance = discord.Embed(title="ID de alianza no encontrado", color=0xFF0000)
        #         embebErrorAlliance.add_field(name="Info:", value="Comprueba que el ID de la alianza {} es correcto".format(allianceId), inline=False)
        #         embebErrorAlliance.set_footer(text="Bot creado por: QueenMirna#9103")
        #         # Mensaje embebido avisando
        #         await ctx.send(embed=embebErrorAlliance)
        #         allianceId = msg.content

        # if allianceExist:
        #     await ctx.send("Introduce el TAG de la alianza")

        #     # This will make sure that the response will only be registered if the following
        #     # conditions are met:
        #     def check(msg):
        #         return msg.author == ctx.author and msg.channel == ctx.channel

        #     try:
        #         msg = await bot.wait_for("message", check=check, timeout=30)
        #     except asyncio.TimeoutError:
        #         await ctx.send("Terminado tiempo de espera, configuración cancelada")

        #     allianceTag = msg.content
        # if allianceExist and guildExist:
        # await ctx.send("Prefix: {} Guild ID: {} Guild TAG:{} Alliance ID: {} Alliance TAG: {}".format(botPrefix))

@bot.command(
    pass_context=True,
    brief="Initial bot setup.",
    help="Configure bot prefix, GuildID and AllianceID.\nExameple: !setup ! w8ofVhjvQWOB3xCczo4szQ hRqowi9bTw6o44R0bsmIUw\nThis will config bot to use '!' as prefix, use 'w8ofVhjvQWOB3xCczo4szQ' as guild ID and 'hRqowi9bTw6o44R0bsmIUw' as allianceID"
)
# Check if have admin perms
@commands.has_permissions(administrator=True)
async def setup(ctx, botPrefix, guildID, allianceID):

    # Guardar la ID de la guild
    DiscordGuildID = ctx.message.guild.id
    # Nombre de las tablas según ID de la guild
    table_users = "{}user".format(DiscordGuildID)
    table_config = "{}config".format(DiscordGuildID)

    setupInfo = discord.Embed(title="Procesando búsqueda en la guild", color=0xFFA500)
    setupInfo.add_field(name="Buscando guild ID:", value="{}".format(guildID), inline=False)
    setupInfo.add_field(name="Buscando alliance ID:", value="{}".format(allianceID), inline=False)
    setupInfo.set_footer(text="Bot creado por: QueenMirna#9103")
    # Mensaje embebido avisando
    await ctx.send(embed=setupInfo)

    guildUrl = 'https://gameinfo.albiononline.com/api/gameinfo/guilds/{}'.format(guildID)
    guildResponse = requests.get(guildUrl)

    if guildResponse.status_code == 200:
        guild_data_json = json.loads(guildResponse.text)
        guildExist = True
    else:
        # Mensaje embebido
        embebErrorGuild = discord.Embed(title="ID de guild no encontrado", color=0xFF0000)
        embebErrorGuild.add_field(name="Info:", value="Compruba que el ID de la guild {} es correcto".format(guildID), inline=False)
        embebErrorGuild.set_footer(text="Bot creado por: QueenMirna#9103")
        # Mensaje embebido avisando
        await ctx.send(embed=embebErrorGuild)

    allianceUrl = 'https://gameinfo.albiononline.com/api/gameinfo/alliances/{}'.format(allianceID)
    allianceResponse = requests.get(allianceUrl)

    try:
        alliance_data_json = json.loads(allianceResponse.text)
        allianceExist = "OK"
    except:
        # Mensaje embebido
        embebErrorAlliance = discord.Embed(title="ID de allianza no encontrada", color=0xFF0000)
        embebErrorAlliance.add_field(name="Info:", value="Compruba que el ID de la allianza {} es correcto".format(guildID), inline=False)
        embebErrorAlliance.set_footer(text="Bot creado por: QueenMirna#9103")
        # Mensaje embebido avisando
        await ctx.send(embed=embebErrorAlliance)
        allianceExist = "KO"

    if guildExist != "KO" and allianceExist != "KO":
        # Mensaje embebido
        embebFindGuild = discord.Embed(title="Confirma que los valores son correctos", color=0x00ff00)
        embebFindGuild.add_field(name="Prefijo del bot:", value="{}".format(botPrefix), inline=False)
        embebFindGuild.add_field(name="Nombre del gremio:", value="{}".format(guild_data_json['Name']), inline=False)
        embebFindGuild.add_field(name="Nombre de la alianza:", value="{}".format(alliance_data_json['AllianceName']), inline=False)
        embebFindGuild.add_field(name="Para continuar escribe:", value="Y", inline=False)
        embebFindGuild.add_field(name="Para cancelar escribe:", value="N", inline=False)
        embebFindGuild.set_footer(text="Bot creado por: QueenMirna#9103")
        # Mensaje embebido avisando
        await ctx.send(embed=embebFindGuild)

        # This will make sure that the response will only be registered if the following
        # conditions are met:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and \
            msg.content.lower() in ["y", "n"]

        try:
            msg = await bot.wait_for("message", check=check, timeout=30)

            if msg.content.lower() == "y":

                # Conectar a la base de datos, se creará si no existe
                # con = sqlite3.connect('example.db')

                # # Create cursor
                # cur = con.cursor()

                # # Se pone "f" delante para que se reconozca las {} como variables
                # # Crear tabla de la configuración de la guild
                # cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_config} (botPrefix text, guildId text, allianceId text)""")

                # # Insertar datos en la tabla
                # cur.execute(f"""INSERT INTO {table_config} (botPrefix, guildId, allianceId) values (?, ?, ?)""", (botPrefix, guildID, allianceID))

                # # Crear tabla de usuarios registrados de la guild
                # cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_users} (userid text, albionnick text)""")
                
                # # Guardar cambios
                # con.commit()

                # # Cerrar conexión
                # con.close()

                await ctx.send("Configuración aplicada")
            else:
                await ctx.send("Configuración caneclada")

        except asyncio.TimeoutError:
            await ctx.send("Terminado tiempo de espera, configuración cancelada")

# !register ARGUMENTO
@bot.command(
    brief="Register user on the guild.",
    help="Register your user.\nExameple: !register QueenMirna"
)
async def register(ctx, username):

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
    embebInfo.add_field(name="Buscando a:", value="{}".format(username), inline=False)
    embebInfo.add_field(name="Tiempo estimado", value="5 minutos", inline=False)
    embebInfo.set_footer(text="Bot creado por: QueenMirna#9103")
    # Mensaje embebido avisando
    await ctx.send(embed=embebInfo)

    # # Petición a la url, y guarda la respuesta
    # API que se usará, con parametrización del usuario
    url = 'https://gameinfo.albiononline.com/api/gameinfo/search?q={}'.format(username)
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
                if player['Name'].lower() == username.lower() and player["GuildId"].lower() == guildID.lower():
                    exist = True

                    # Mensaje embebido
                    embebFindGuild = discord.Embed(title="Jugador encontrado", color=0x00ff00)
                    embebFindGuild.add_field(name="Bievenid@:", value="{}".format(username), inline=False)
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
                if player['Name'].lower() == username.lower() and player["AllianceId"].lower() == allianceID.lower():
                    exist = True
                    # Mensaje embebido
                    embebFindAlliance = discord.Embed(title="Jugador encontrado", color=0x8c004b)
                    embebFindAlliance.add_field(name="Bievenid@:", value="{}".format(username), inline=False)
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
                        embebNotFound.add_field(name="El jugador:", value="{}\nSi crees que es un error contacta con un oficial".format(username), inline=False)
                        embebNotFound.set_footer(text="Bot creado por: QueenMirna#9103")
                        # Mensaje embebido avisando
                        await ctx.send(embed=embebNotFound)
                        break
        
        # No existe ningún jugador con ese nombre, NO devuelve resultados la lista
        else:
            # Mensaje embebido
            embebNotFound = discord.Embed(title="Jugador no encontrado", color=0xFF0000)
            embebNotFound.add_field(name="El jugador:", value="{}\nSi crees que es un error contacta con un oficial".format(username), inline=False)
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
