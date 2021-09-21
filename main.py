import os
import discord
from discord.utils import get
import nextcord
import sqlite3
from dotenv import load_dotenv
from nextcord.ext import commands
import requests
import json
import asyncio
from datetime import datetime

# Load env variables file
load_dotenv()

# Get env var and save to var
TOKEN = os.environ.get("TOKEN")


botPrefix = "!"
bot = commands.Bot(command_prefix='{}'.format(botPrefix))

# Iniciar bot con el token introducido
@bot.event
async def on_ready():
    # Mensaje mostrando que está iniciado
    print('Logged in as {0.user}'.format(bot))

@bot.command(
    pass_context=True,
    brief="Initial bot setup.",
    help="Configure bot prefix, Guild ID, Guild TAG, Alliance ID and Alliance TAG (Will be get from the Alliance ID)."
)
# Check if have admin perms
@commands.has_permissions(administrator=True)
async def setup(ctx):

    # Guardar la ID de la guild
    DiscordGuildID = ctx.message.guild.id
    # Nombre de las tablas según ID de la guild
    table_users = "registedUsers{}".format(DiscordGuildID)
    table_config = "DiscordServersConfig"

    botPrefixOk = False
    while not botPrefixOk:
        await ctx.send("Introduce el prefijo del bot")

        # This will make sure that the response will only be registered if the following
        # conditions are met:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        try:
            msg = await bot.wait_for("message", check=check, timeout=30)
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
            msg = await bot.wait_for("message", check=check, timeout=30)
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
                    msg = await bot.wait_for("message", check=check, timeout=30)
                    if msg.content.lower() == "y":
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

    if not guildResponse:
        return

    guildTag = False
    while not guildTag:
        await ctx.send("Introduce el TAG de la Guild")

        # This will make sure that the response will only be registered if the following
        # conditions are met:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        try:
            msg = await bot.wait_for("message", check=check, timeout=30)

            if len(msg.clean_content) == 3:
                guildTag = True
                guildTagResponse = True
                guildTagString = msg.content
            else:
                await ctx.send("El TAG debe ser de 3 caracteres")
                guildTagResponse = False
        except asyncio.TimeoutError:
            await ctx.send("Terminado tiempo de espera, configuración cancelada")
            guildTag = True
            guildTagResponse = False

    if not guildTagResponse:
        return

    guildRol = False
    while not guildRol:
        await ctx.send("Introduce el nombre del ROL que se asignará a los miembros de la guild al registrarse.")

        # This will make sure that the response will only be registered if the following
        # conditions are met:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        try:
            msg = await bot.wait_for("message", check=check, timeout=30)

            if get(ctx.guild.roles, name="{}".format(msg.content)):
                guildRol = True
                guildRolResponse = True
                guildRol = msg.content
            else:
                await ctx.send("No existe ningún con ROL con ese nombre")
                guildRolResponse = False
        except asyncio.TimeoutError:
            await ctx.send("Terminado tiempo de espera, configuración cancelada")
            guildRol = True
            guildRolResponse = False

    if not guildRolResponse:
        return

    await ctx.send("¿Quieres añadir alianza? 'Y' or 'N'")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
        msg.content.lower() in ["y", "n"]

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        if msg.content.lower() == "y":

            allianceExist = False
            while not allianceExist:
                await ctx.send("Introduce la ID de la alianza")

                # This will make sure that the response will only be registered if the following
                # conditions are met:
                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel

                try:
                    msg = await bot.wait_for("message", check=check, timeout=30)
                    allianceResponse = True
                except asyncio.TimeoutError:
                    await ctx.send("Terminado tiempo de espera, configuración cancelada")
                    allianceExist = True
                    allianceResponse = False

                if allianceResponse:
                    allianceId = msg.content

                    guildUrl = 'https://gameinfo.albiononline.com/api/gameinfo/alliances/{}'.format(allianceId)
                    allianceResponse = requests.get(guildUrl)

                    if allianceResponse.status_code == 200:
                        alliance_data_json = json.loads(allianceResponse.text)
                        # Mensaje embebido
                        embebAllianceGuild = discord.Embed(title="Comprobación", color=0xFFA500)
                        embebAllianceGuild.add_field(name="Info", value="Tu alianza se llama: **{}**".format(alliance_data_json['AllianceName']), inline=False)
                        embebAllianceGuild.add_field(name="¿Es correcto?", value="Si es así, escribe **Y**, para continuar, sino **N** para introducir uno nuevo")
                        embebAllianceGuild.set_footer(text="Bot creado por: QueenMirna#9103")
                        # Mensaje embebido avisando
                        await ctx.send(embed=embebAllianceGuild)

                        # This will make sure that the response will only be registered if the following
                        # conditions are met:
                        def check(msg):
                            return msg.author == ctx.author and msg.channel == ctx.channel and \
                            msg.content.lower() in ["y", "n"]

                        try:
                            msg = await bot.wait_for("message", check=check, timeout=30)
                            if msg.content.lower() == "y":
                                allianceExist = True
                                allianceResponse = True

                        except asyncio.TimeoutError:
                            await ctx.send("Terminado tiempo de espera, configuración cancelada")
                            allianceExist = True
                            allianceResponse = False
                    else:
                        # Mensaje embebido
                        embebErrorGuild = discord.Embed(title="ID de alianza no encontrado", color=0xFF0000)
                        embebErrorGuild.add_field(name="Info:", value="Comprueba que el ID de la alianza es: {}".format(allianceId), inline=False)
                        embebErrorGuild.set_footer(text="Bot creado por: QueenMirna#9103")
                        # Mensaje embebido avisando
                        await ctx.send(embed=embebErrorGuild)

            if not allianceResponse:
                return

            allianceRol = False
            while not allianceRol:
                await ctx.send("Introduce el nombre del ROL que se asignará a los miembros de la guild al registrarse.")

                # This will make sure that the response will only be registered if the following
                # conditions are met:
                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel
                
                try:
                    msg = await bot.wait_for("message", check=check, timeout=30)

                    if get(ctx.guild.roles, name="{}".format(msg.content)):
                        allianceRol = True
                        allianceRolResponse = True
                        allianceRol = msg.content
                    else:
                        await ctx.send("No existe ningún con ROL con ese nombre")
                        allianceRolResponse = False
                except asyncio.TimeoutError:
                    await ctx.send("Terminado tiempo de espera, configuración cancelada")
                    allianceRol = True
                    allianceRolResponse = False
            
            # allianceTag = False
            # while not allianceTag:
            #     await ctx.send("Introduce el TAG de la Alianza")

            #     # This will make sure that the response will only be registered if the following
            #     # conditions are met:
            #     def check(msg):
            #         return msg.author == ctx.author and msg.channel == ctx.channel
                
            #     try:
            #         msg = await bot.wait_for("message", check=check, timeout=30)

            #         if len(msg.clean_content) > 4:
            #             allianceTag = True
            #             allianceTagResponse = True
            #             allianceTagString = msg.content
            #         else:
            #             await ctx.send("El TAG no debe ser mayor de 4 caracteres")
            #             allianceTagResponse = False
            #     except asyncio.TimeoutError:
            #         await ctx.send("Terminado tiempo de espera, configuración cancelada")
            #         allianceTag = True
            #         allianceTagResponse = False

            # if not allianceTagResponse:
            #     return

            if not allianceRolResponse:
                return

        else:
            allianceExist = False

    except asyncio.TimeoutError:
        await ctx.send("Terminado tiempo de espera, configuración cancelada")
        return

    if guildTag and allianceExist:
        # Mensaje embebido
        embebFindGuild = discord.Embed(title="Confirma que los valores son correctos", color=0x00ff00)
        embebFindGuild.add_field(name="Prefijo del bot:", value="{}".format(botPrefix), inline=False)
        embebFindGuild.add_field(name="Nombre del gremio:", value="{}".format(guild_data_json['Name']), inline=False)
        embebFindGuild.add_field(name="TAG del gremio:", value="{}".format(guildTagString), inline=False)
        embebFindGuild.add_field(name="ROL del gremio:", value="{}".format(guildRol), inline=False)
        embebFindGuild.add_field(name="Nombre de la alianza:", value="{}".format(alliance_data_json['AllianceName']), inline=False)
        embebFindGuild.add_field(name="TAG de la alianza:", value="{}".format(alliance_data_json['AllianceTag']), inline=False)
        embebFindGuild.add_field(name="ROL de la alianza:", value="{}".format(allianceRol), inline=False)
        embebFindGuild.add_field(name="¿Es correcto?", value="Si es así, escribe **Y**, para continuar, sino **N** para introducir uno nuevo")
        embebFindGuild.set_footer(text="Bot creado por: QueenMirna#9103")
        # Mensaje embebido avisando
        await ctx.send(embed=embebFindGuild)

    if guildTag and not allianceExist:
        embebFindGuild = discord.Embed(title="Confirma que los valores son correctos", color=0x00ff00)
        embebFindGuild.add_field(name="Prefijo del bot:", value="{}".format(botPrefix), inline=False)
        embebFindGuild.add_field(name="Nombre del gremio:", value="{}".format(guild_data_json['Name']), inline=False)
        embebFindGuild.add_field(name="TAG del gremio:", value="{}".format(guildTagString), inline=False)
        embebFindGuild.add_field(name="ROL de la guild:", value="{}".format(guildRol), inline=False)
        embebFindGuild.add_field(name="¿Es correcto?", value="Si es así, escribe **Y**, para continuar, sino **N** para introducir uno nuevo")
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

            #Conectar a la base de datos, se creará si no existe
            con = sqlite3.connect('example.db')

            # Create cursor
            cur = con.cursor()

            # Se pone "f" delante para que se reconozca las {} como variables
            # Crear tabla de la configuración de la guild
            cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_config} 
                        (guildId TEXT PRIMARY KEY,
                        botPrefix TEXT,
                        guildTagString TEXT,
                        guildRol TEXT,
                        allianceId TEXT,
                        allianceTagString TEXT,
                        allianceRol TEXT)"""
                        )

            # Insertar datos en la tabla
            if allianceExist:
                cur.execute(f"""INSERT INTO {table_config} (guildId, botPrefix, guildTagString, guildRol, allianceId, allianceTagString, allianceRol) 
                VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT(guildId) DO UPDATE SET
                guildId="{guildId}",
                botPrefix="{botPrefix}",
                guildTagString="{guildTagString}",
                guildRol="{guildRol}",
                allianceId="{allianceId}",
                allianceTagString="{ alliance_data_json['AllianceTag']}",
                allianceRol="{allianceRol}"
                """, (guildId, botPrefix, guildTagString, guildRol, allianceId, alliance_data_json['AllianceTag'], allianceRol)
                )
            else:
                cur.execute(f"""INSERT INTO {table_config} (guildId, botPrefix, guildTagString, guildRol, allianceId, allianceTagString, allianceRol) 
                VALUES (?, ?, ?, ?, 'none', 'none', 'none') ON CONFLICT(guildId) DO UPDATE SET
                guildId="{guildId}",
                botPrefix="{botPrefix}",
                guildTagString="{guildTagString}",
                guildRol="{guildRol}"
                """, (guildId, botPrefix, guildTagString, guildRol)
                )

            # Crear tabla de usuarios registrados de la guild
            cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_users} (userid text, albionnick text);""")
            
            # Guardar cambios
            con.commit()

            # Cerrar conexión
            con.close()

            await ctx.send("Configuración aplicada")
        else:
            await ctx.send("Configuración caneclada")

    except asyncio.TimeoutError:
        await ctx.send("Terminado tiempo de espera, configuración cancelada")

# !register ARGUMENTO
@bot.command(
    pass_context=True,
    brief="Register user on the guild.",
    help="Register your user.\nExameple: !register QueenMirna"
)
async def register(ctx, username):

    memberId = ctx.message.author.id
    con = sqlite3.connect('example.db')

    cur = con.cursor()

    DiscordGuildID = ctx.message.guild.id
    table_users = "registedUsers{}".format(DiscordGuildID)

    try:
        checkUser = cur.execute(f"""SELECT userid FROM {table_users} where userid={memberId}""").fetchall()[0][0]
    except IndexError:
        checkUser = False
        pass
        

    if checkUser:
        checkNick = cur.execute(f"""SELECT albionnick FROM {table_users} where userid={memberId}""").fetchall()[0][0]

        embebInfo = discord.Embed(title="Ya estás registrado", color=0xff0000)
        embebInfo.add_field(name="Registrado con el usuario", value="{}".format(checkNick), inline=False)
        embebInfo.add_field(name="Para eliminar el registro", value="!unregister", inline=False)
        embebInfo.set_footer(text="Bot creado por: QueenMirna#9103")
        # Mensaje embebido avisando
        await ctx.send(embed=embebInfo)

        con.close()

        return

    else:

        con = sqlite3.connect('example.db')

        cur = con.cursor()

        try:
            registerGuildId = cur.execute('SELECT guildId FROM DiscordServersConfig').fetchall()[0][0]
            registerGuildTag = cur.execute('SELECT guildTagString FROM DiscordServersConfig').fetchall()[0][0]
            registerGuildRol = cur.execute('SELECT guildRol FROM DiscordServersConfig').fetchall()[0][0]
            registerAllianceId = cur.execute('SELECT allianceId FROM DiscordServersConfig').fetchall()[0][0]
            registerAllianceTag = cur.execute('SELECT allianceTagString FROM DiscordServersConfig').fetchall()[0][0]
            registerAllianceRol = cur.execute('SELECT allianceRol FROM DiscordServersConfig').fetchall()[0][0]
        except sqlite3.OperationalError:
            await ctx.send("El bot aún no está configurado, use !setup para configurarlo, si no tiene permisos, contacte con el administrador.")
            return

        con.close()

        # Obtiene el ID del autor del mensaje
        member = ctx.message.author

        embebInfo = discord.Embed(title="Procesando búsqueda", color=0xFFA500)
        embebInfo.add_field(name="Buscando a:", value="{}".format(username), inline=False)
        embebInfo.add_field(name="Tiempo estimado", value="5 minutos", inline=False)
        embebInfo.set_footer(text="Bot creado por: QueenMirna#9103")
        # Mensaje embebido avisando
        await ctx.send(embed=embebInfo)

        # # Petición a la url, y guarda la respuesta
        # API que se usará, con parametrización del usuario
        url = 'https://gameinfo.albiononline.com/api/gameinfo/search?q={}'.format(username)
        response = requests.get(url)

        if response.status_code == 200:
            # Transforma la info en texto plano a json
            data_json = json.loads(response.text)
            exist = False

            # Si players existe en data_json
            if data_json.get('players'):

                for player in data_json['players']:
                    
                    # INFO - Guild
                    # Si player es igual al nombre del jugador pasado devolver datos
                    if player['Name'].lower() == username.lower() and player["GuildId"] == registerGuildId:
                        exist = True

                        # Mensaje embebido
                        embebFindGuild = discord.Embed(title="Jugador encontrado", color=0x00ff00)
                        embebFindGuild.add_field(name="Bievenid@:", value="{}".format(username), inline=False)
                        embebFindGuild.add_field(name="Rol asignado:", value="{}".format(registerGuildRol), inline=False)
                        embebFindGuild.add_field(name="Nick actualizado a:", value="[{}] {}".format(registerGuildTag ,player['Name']), inline=False)
                        embebFindGuild.set_footer(text="Bot creado por: QueenMirna#9103")
                        # Mensaje embebido avisando
                        await ctx.send(embed=embebFindGuild)

                        # Asignar rol
                        DiscordGuildID = bot.get_guild(ctx.message.guild.id)
                        role = discord.utils.get(DiscordGuildID.roles, name="{}".format(registerGuildRol))
                        await member.add_roles(role)

                        # Cambiar nombre
                        try:
                            await member.edit(nick="[{}] {}".format(registerGuildTag ,player['Name']))
                        except nextcord.errors.Forbidden:
                            embebInfo = discord.Embed(title="Error de permisos", color=0xff0000)
                            embebInfo.add_field(name="Permisos faltantes", value="Manage Nicknames, si eres un admin puede ser que el bot no tenga permisos de editar nicks a admins, pero si a usuarios básicos", inline=False)
                            embebInfo.set_footer(text="Bot creado por: QueenMirna#9103")

                            # Mensaje embebido avisando
                            await ctx.send(embed=embebInfo)
                            pass

                        # Guardar la ID de la guild
                        DiscordGuildID = ctx.message.guild.id
                        # Nombre de las tablas según ID de la guild
                        table_users = "registedUsers{}".format(DiscordGuildID)

                        con = sqlite3.connect('example.db')

                        # Create cursor
                        cur = con.cursor()

                        memberId = ctx.message.author.id
                        # Se pone "f" delante para que se reconozca las {} como variables
                        # Insertar datos en la tabla
                        cur.execute(f"""INSERT INTO {table_users} (userid, albionnick) values (?, ?)""", (memberId, username))
                        
                        # Guardar cambios
                        con.commit()

                        # Cerrar conexión
                        con.close()

                        break
                    
                    # INFO - Alliance
                    if player['Name'].lower() == username.lower() and player["AllianceId"] == registerAllianceId:
                        exist = True
                        # Mensaje embebido
                        embebFindAlliance = discord.Embed(title="Jugador encontrado", color=0x8c004b)
                        embebFindAlliance.add_field(name="Bievenid@:", value="{}".format(username), inline=False)
                        embebFindAlliance.add_field(name="Rol asignado:", value="{}".format(registerAllianceRol), inline=False)
                        embebFindAlliance.add_field(name="Nick actualizado a:", value="[{}] {}".format(registerAllianceTag ,player['Name']), inline=False)
                        embebFindAlliance.set_footer(text="Bot creado por: QueenMirna#9103")
                        # Mensaje embebido avisando
                        await ctx.send(embed=embebFindAlliance)

                        # Asignar rol
                        DiscordGuildID = bot.get_guild(ctx.message.guild.id)
                        role = discord.utils.get(DiscordGuildID.roles, name="{}".format(registerAllianceRol))
                        await member.add_roles(role)

                        # Cambiar nombre
                        try:
                            await member.edit(nick="[{}] {}".format(registerAllianceTag ,player['Name']))
                        except nextcord.errors.Forbidden:
                            embebInfo = discord.Embed(title="Error de permisos", color=0xff0000)
                            embebInfo.add_field(name="Permisos faltantes", value="Manage Nicknames, si eres un admin puede ser que el bot no tenga permisos de editar nicks a admins, pero si a usuarios básicos", inline=False)
                            embebInfo.set_footer(text="Bot creado por: QueenMirna#9103")

                            # Mensaje embebido avisando
                            await ctx.send(embed=embebInfo)
                            pass

                        # Nombre de las tablas según ID de la guild
                        table_users = "registedUsers{}".format(DiscordGuildID)

                        con = sqlite3.connect('example.db')

                        # Create cursor
                        cur = con.cursor()

                        memberId = ctx.message.author.id
                        # Se pone "f" delante para que se reconozca las {} como variables
                        # Insertar datos en la tabla
                        cur.execute(f"""INSERT INTO {table_users} (userid, albionnick) values (?, ?)""", (memberId, username))
                        
                        # Guardar cambios
                        con.commit()

                        # Cerrar conexión
                        con.close()

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
            embebFindAlliance = discord.Embed(title="Error al procesar la solicitud", color=0xFF0000)
            embebFindAlliance.add_field(name="Info:", value="Inténtalo de nuevo", inline=False)
            # Mensaje embebido avisando
            await ctx.send(embed=embebFindAlliance)

            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y | %H:%M:%S")

            print("{} - API Error {}".format(dt_string, response.status_code))

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
    table_users = "registedUsers{}".format(DiscordGuildID)

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

# Token del bot a usar
bot.run(TOKEN)
