import discord
from discord.ext import commands
import asyncio
import sqlite3
import requests
import json
from discord.utils import get


class ConfigCog(commands.Cog, name="Config Commands"):
    def __init__(self, bot):
        self.bot = bot
      
    @commands.command(
        name='setup',
        pass_context=True,
        brief="Initial bot setup.",
        help="Configure bot prefix, Guild ID, Guild TAG, Alliance ID and Alliance TAG (Will be get from the Alliance ID)."
    )
    # Check if have admin perms
    @commands.has_permissions(
                              administrator=True
                              )
    async def setup(self, ctx):
        # Guardar la ID de la guild
        DiscordGuildID = ctx.message.guild.id
        # Nombre de las tablas según ID de la guild
        table_users = "registeredUsers{}".format(DiscordGuildID)
        table_config = "DiscordServersConfig"

        botPrefixOk = False
        while not botPrefixOk:
            await ctx.send("Introduce el prefijo del bot")

            # This will make sure that the response will only be registered if the following
            # conditions are met:
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
            
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=30)
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
                msg = await self.bot.wait_for("message", check=check, timeout=30)
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
                        msg = await self.bot.wait_for("message", check=check, timeout=30)
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
                msg = await self.bot.wait_for("message", check=check, timeout=30)

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
                msg = await self.bot.wait_for("message", check=check, timeout=30)

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
            msg = await self.bot.wait_for("message", check=check, timeout=30)
            if msg.content.lower() == "y":

                allianceExist = False
                while not allianceExist:
                    await ctx.send("Introduce la ID de la alianza")

                    # This will make sure that the response will only be registered if the following
                    # conditions are met:
                    def check(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel

                    try:
                        msg = await self.bot.wait_for("message", check=check, timeout=30)
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
                                msg = await self.bot.wait_for("message", check=check, timeout=30)
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
                        msg = await self.bot.wait_for("message", check=check, timeout=30)

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
            msg = await self.bot.wait_for("message", check=check, timeout=30)

            if msg.content.lower() == "y":

                #Conectar a la base de datos, se creará si no existe
                con = sqlite3.connect('example.db')

                # Create cursor
                cur = con.cursor()

                # Se pone "f" delante para que se reconozca las {} como variables
                # Crear tabla de la configuración de la guild
                cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_config} 
                            (discordGuildId TEXT PRIMARY KEY,
                            botPrefix TEXT,
                            guildId TEXT,
                            guildTagString TEXT,
                            guildRol TEXT,
                            allianceId TEXT,
                            allianceTagString TEXT,
                            allianceRol TEXT)"""
                            )

                # Insertar datos en la tabla
                if allianceExist:
                    cur.execute(f"""INSERT INTO {table_config} (
                        discordGuildId,
                        botPrefix,
                        guildId,
                        guildTagString,
                        guildRol,
                        allianceId,
                        allianceTagString,
                        allianceRol) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(discordGuildId) DO UPDATE SET
                    discordGuildId="{DiscordGuildID}",
                    botPrefix="{botPrefix}",
                    guildId="{guildId}",
                    guildTagString="{guildTagString}",
                    guildRol="{guildRol}",
                    allianceId="{allianceId}",
                    allianceTagString="{ alliance_data_json['AllianceTag']}",
                    allianceRol="{allianceRol}"
                    """, (DiscordGuildID, botPrefix, guildId, guildTagString, guildRol, allianceId, alliance_data_json['AllianceTag'], allianceRol)
                    )
                else:
                    cur.execute(f"""INSERT INTO {table_config} (
                        discordGuildId,
                        guildId,
                        botPrefix,
                        guildTagString,
                        guildRol,
                        allianceId,
                        allianceTagString,
                        allianceRol) 
                    VALUES (?, ?, ?, ?, ?, 'none', 'none', 'none') ON CONFLICT(discordGuildId) DO UPDATE SET
                    discordGuildId="{DiscordGuildID}",
                    botPrefix="{botPrefix}",
                    guildId="{guildId}",
                    guildTagString="{guildTagString}",
                    guildRol="{guildRol}"
                    """, (DiscordGuildID, guildId, botPrefix, guildTagString, guildRol)
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

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(ConfigCog(bot))