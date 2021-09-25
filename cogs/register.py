import discord
from discord.ext import commands
from nextcord.ext.commands.context import P
import requests
import json
from datetime import datetime
import nextcord
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

dbName = os.environ.get("DBNAME")
table_config = os.environ.get("TABLE_CONFIG")
table_register = os.environ.get("TABLE_USER")
table_blacklist = os.environ.get("TABLE_BLACKLIST")

class RegisterCog(commands.Cog, name="Register Command"):
    def __init__(self, bot):
        self.bot = bot

    # !register ARGUMENTO
    @commands.command(
        name="register",
        pass_context=True,
        brief="Register user on the guild.",
        help="Register your user.\nExameple: !register QueenMirna"
    )
    async def register(self, ctx, username):

        memberId = ctx.message.author.id
        con = sqlite3.connect(dbName)

        cur = con.cursor()

        DiscordGuildID = ctx.message.guild.id

        try:
            checkUser = cur.execute(f"""SELECT userid FROM {table_register} where userid={memberId} AND discordGuildIdFK={DiscordGuildID}""").fetchall()[0][0]
        except (IndexError, sqlite3.OperationalError):
            checkUser = False
            pass
            

        if checkUser:
            checkNick = cur.execute(f"""SELECT albionnick FROM {table_register} where userid={memberId} AND discordGuildIdFK={DiscordGuildID}""").fetchall()[0][0]

            embebInfo = discord.Embed(title="Ya estás registrado", color=0xff0000)
            embebInfo.add_field(name="Registrado con el usuario", value="{}".format(checkNick), inline=False)
            embebInfo.add_field(name="Para eliminar el registro", value="!unregister", inline=False)
            embebInfo.set_footer(text="Bot creado por: QueenMirna#9103")
            # Mensaje embebido avisando
            await ctx.send(embed=embebInfo)

            con.close()

            return

        else:

            con = sqlite3.connect(dbName)

            cur = con.cursor()

            try:
                registerGuildId = cur.execute(f"""SELECT guildId FROM DiscordServersConfig where discordGuildId={DiscordGuildID}""").fetchall()[0][0]
                registerGuildTag = cur.execute(f"""SELECT guildTag FROM DiscordServersConfig where discordGuildId={DiscordGuildID}""").fetchall()[0][0]
                registerGuildRol = cur.execute(f"""SELECT guildRol FROM DiscordServersConfig where discordGuildId={DiscordGuildID}""").fetchall()[0][0]
                registerAllianceId = cur.execute(f"""SELECT allianceId FROM DiscordServersConfig where discordGuildId={DiscordGuildID}""").fetchall()[0][0]
                registerAllianceTag = cur.execute(f"""SELECT allianceTag FROM DiscordServersConfig where discordGuildId={DiscordGuildID}""").fetchall()[0][0]
                registerAllianceRol = cur.execute(f"""SELECT allianceRol FROM DiscordServersConfig where discordGuildId={DiscordGuildID}""").fetchall()[0][0]
            except (sqlite3.OperationalError, IndexError):
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
                            try:
                              DiscordGuildID = self.bot.get_guild(ctx.message.guild.id)
                              role = discord.utils.get(DiscordGuildID.roles, name="{}".format(registerGuildRol))
                              await member.add_roles(role)

                            except nextcord.errors.Forbidden:
                              embebPermissionError = discord.Embed(title="Error de permisos", color=0xff0000)
                              embebPermissionError.add_field(name="Permisos faltantes", value="***Manage rol***, si eres un admin puede ser que el bot no tenga permisos para asignar roles o que el rol de bot esté por debajo de los roles a asignar, asegurate que está por encima de los roles que quieres asignar")
                              embebPermissionError.set_footer(text="Bot creado por: QueenMirna#9103")

                              # Mensaje embebido avisando
                              await ctx.send(embed=embebPermissionError)
                              

                            # Cambiar nombre
                            try:
                                await member.edit(nick="[{}] {}".format(registerGuildTag ,player['Name']))
                            except nextcord.errors.Forbidden:
                                embebInfo = discord.Embed(title="Error de permisos", color=0xff0000)
                                embebInfo.add_field(name="Permisos faltantes", value="***Manage Nicknames***, si eres un admin puede ser que el bot no tenga permisos de editar nicks a admins, pero si a usuarios básicos", inline=False)
                                embebInfo.set_footer(text="Bot creado por: QueenMirna#9103")

                                # Mensaje embebido avisando
                                await ctx.send(embed=embebInfo)
                                pass

                            # Guardar la ID de la guild
                            DiscordGuildID = ctx.message.guild.id

                            con = sqlite3.connect(dbName)

                            # Create cursor
                            cur = con.cursor()

                            memberId = ctx.message.author.id
                            # Se pone "f" delante para que se reconozca las {} como variables
                            # Insertar datos en la tabla
                            cur.execute(f"""INSERT INTO {table_register} (userid, discordGuildIdFK, albionnick) values (?, ?, ?)""", (memberId, DiscordGuildID, username))
                            
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
                            DiscordGuildID = self.bot.get_guild(ctx.message.guild.id)
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

                            con = sqlite3.connect(dbName)

                            # Create cursor
                            cur = con.cursor()

                            memberId = ctx.message.author.id
                            # Se pone "f" delante para que se reconozca las {} como variables
                            # Insertar datos en la tabla
                            cur.execute(f"""INSERT INTO {table_register} (userid, discordGuildIdFK, albionnick) values (?, ?, ?)""", (memberId, DiscordGuildID, username))
                            
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
                embebFindAlliance.set_footer(text="Bot creado por: QueenMirna#9103")
                # Mensaje embebido avisando
                await ctx.send(embed=embebFindAlliance)

                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y | %H:%M:%S")

                print("{} - API Error {}".format(dt_string, response.status_code))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embebRegisterError = discord.Embed(title="Error", color=0xFF0000)
            embebRegisterError.add_field(name="Info:", value="Introduce un nombre de usuario", inline=False)
            embebRegisterError.set_footer(text="Bot creado por: QueenMirna#9103")
            # Mensaje embebido avisando
            await ctx.send(embed=embebRegisterError)

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(RegisterCog(bot))