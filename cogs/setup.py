import discord
from discord.ext import commands
import asyncio
import sqlite3
import requests
import json
from discord.utils import get
import os
from dotenv import load_dotenv

load_dotenv()

dbName = os.environ.get("DBNAME")
table_config = os.environ.get("TABLE_CONFIG")
table_register = os.environ.get("TABLE_USER")
table_blacklist = os.environ.get("TABLE_BLACKLIST")

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
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'}
                guildResponse = requests.get(guildUrl, headers=headers)

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
                    embebErrorGuild = discord.Embed(title="Error", color=0xFF0000)
                    embebErrorGuild.add_field(name="Info:", value="ID de guild no encontrado, comprueba que el ID de la guild es: {}".format(guildId), inline=False)
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

                if len(msg.clean_content) <= 4:
                    guildTag = True
                    guildTagResponse = True
                    guildTagString = msg.content
                else:
                    await ctx.send("El TAG debe ser de máximo 4 caracteres")
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

                        allianceUrl = 'https://gameinfo.albiononline.com/api/gameinfo/alliances/{}'.format(allianceId)
                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'}
                        allianceResponse = requests.get(allianceUrl, headers=headers)

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
                            embebErrorGuild = discord.Embed(title="Error", color=0xFF0000)
                            embebErrorGuild.add_field(name="Info:", value="ID de alianza no encontrado, comprueba que el ID de la alianza es: {}".format(allianceId), inline=False)
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
                con = sqlite3.connect(dbName)

                # Create cursor
                cur = con.cursor()

                # Se pone "f" delante para que se reconozca las {} como variables
                # Insertar datos en la tabla
                if allianceExist:
                    cur.execute(f"""INSERT INTO {table_config} (
                        discordGuildId,
                        botPrefix,
                        guildId,
                        guildTag,
                        guildRol,
                        allianceId,
                        allianceTag,
                        allianceRol) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(discordGuildId) DO UPDATE SET
                    discordGuildId="{DiscordGuildID}",
                    botPrefix="{botPrefix}",
                    guildId="{guildId}",
                    guildTag="{guildTagString}",
                    guildRol="{guildRol}",
                    allianceId="{allianceId}",
                    allianceTag="{ alliance_data_json['AllianceTag']}",
                    allianceRol="{allianceRol}"
                    """, (DiscordGuildID, botPrefix, guildId, guildTagString, guildRol, allianceId, alliance_data_json['AllianceTag'], allianceRol)
                    )
                else:
                    cur.execute(f"""INSERT INTO {table_config} (
                        discordGuildId,
                        botPrefix,
                        guildId,
                        guildTag,
                        guildRol,
                        allianceId,
                        allianceTag,
                        allianceRol) 
                    VALUES (?, ?, ?, ?, ?, 'none', 'none', 'none') ON CONFLICT(discordGuildId) DO UPDATE SET
                    discordGuildId="{DiscordGuildID}",
                    botPrefix="{botPrefix}",
                    guildId="{guildId}",
                    guildTag="{guildTagString}",
                    guildRol="{guildRol}"
                    """, (DiscordGuildID, botPrefix, guildId, guildTagString, guildRol)
                    )
                
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