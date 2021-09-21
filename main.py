import os
import discord
import nextcord
import sqlite3
from dotenv import load_dotenv
from nextcord.ext import commands
import requests
import json
from datetime import datetime
import sys, traceback

# Load env variables file
load_dotenv()

# Get env var and save to var
TOKEN = os.environ.get("TOKEN")


def botPrefixes(bot, message):

    table_config = "DiscordServersConfig"

    DiscordGuildID = message.guild.id

    con = sqlite3.connect('example.db')

    cur = con.cursor()

    try:
        botPrefix = cur.execute(f"""SELECT botPrefix FROM {table_config} where discordGuildId={DiscordGuildID}""").fetchall()[0]
    except (sqlite3.OperationalError, IndexError):
        botPrefix = "!"
    
    con.close()

    return botPrefix[0]

bot = commands.Bot(
    command_prefix= (botPrefixes)
    )

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
    table_users = "registeredUsers{}".format(DiscordGuildID)

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
            registerGuildId = cur.execute(f"""SELECT guildId FROM DiscordServersConfig where guildId={DiscordGuildID}""").fetchall()[0][0]
            registerGuildTag = cur.execute(f"""SELECT guildTagString FROM DiscordServersConfig where guildId={DiscordGuildID}""").fetchall()[0][0]
            registerGuildRol = cur.execute(f"""SELECT guildRol FROM DiscordServersConfig where guildId={DiscordGuildID}""").fetchall()[0][0]
            registerAllianceId = cur.execute(f"""SELECT allianceId FROM DiscordServersConfig where guildId={DiscordGuildID}""").fetchall()[0][0]
            registerAllianceTag = cur.execute(f"""SELECT allianceTagString FROM DiscordServersConfig where guildId={DiscordGuildID}""").fetchall()[0][0]
            registerAllianceRol = cur.execute(f"""SELECT allianceRol FROM DiscordServersConfig where guildId={DiscordGuildID}""").fetchall()[0][0]
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
                        table_users = "registeredUsers{}".format(DiscordGuildID)

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
                        table_users = "registeredUsers{}".format(DiscordGuildID)

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
    table_users = "registereddUsers{}".format(DiscordGuildID)

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
                    'cogs.setup'
                    ]

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

# Token del bot a usar
bot.run(TOKEN, reconnect=True)
