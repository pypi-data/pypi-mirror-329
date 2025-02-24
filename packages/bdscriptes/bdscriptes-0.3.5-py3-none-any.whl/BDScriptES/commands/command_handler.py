from .process_title import process_title
from .process_description import process_description
from .process_color import process_color
from .process_author import process_author
from .process_author_icon import process_author_icon
from .process_author_url import process_author_url
from .process_image import process_image
from .process_thumbnail import process_thumbnail
from .process_title_url import process_title_url
from .process_message import process_message
from .process_conditions import process_conditions
from .process_var import procesar_variables
from .process_delete_message import process_delete_message
from .process_message_user_id import process_message_user_id
from .process_guild_id import process_guild_id  
from .process_channel_id import process_channel_id  # Importando la función
from BDScriptES.utils.process_text import process_text
from BDScriptES.utils.error_handler import handle_error
import discord
from discord.ext import commands


class CommandHandler:
    def __init__(self, bot):
        self.bot = bot
        self.commands_dict = {}
        self.on_message_commands = []  # Lista para $onMessage

        # Agregar el listener de mensajes globalmente
        bot.event(self.on_message)

    def new_command(self, name, type, code):
        """
        Registra un nuevo comando, diferenciando entre comandos normales y $onMessage.
        """
        if type == "$onMessage":
            # Se ignora el nombre y se añade a la lista de comandos que se ejecutan con cualquier mensaje
            self.on_message_commands.append({'code': code})
        else:
            # Se registra un comando normal con su nombre
            self.commands_dict[name] = {'type': type, 'code': code}

            @self.bot.command(name=name)
            async def dynamic_command(ctx):
                await self.execute_command(ctx, self.commands_dict[name]['code'], type)

    async def execute_command(self, ctx, code, command_type="sendMessage", message_content=None):
        """
        Procesa y ejecuta un comando según su tipo.
        """
        try:
            # Procesar funciones antes de evaluar el mensaje
            processed_code = await process_guild_id(code, ctx)
            processed_code = process_message_user_id(processed_code, ctx)
            processed_code = process_channel_id(processed_code, ctx)  # ✅ Implementación de $channelID
            processed_code = process_message(processed_code, message_content or ctx.message.content)
            processed_code = procesar_variables(processed_code)
            processed_code = process_conditions(processed_code)
            processed_code = await process_delete_message(processed_code, ctx, self.bot)
            
            # Extraer texto fuera de funciones
            plain_text = process_text(processed_code)

            if command_type in ["sendMessage", "$onMessage"]:
                # Procesar títulos, descripciones, etc.
                titles = process_title(processed_code)
                descriptions = process_description(processed_code)
                colors = process_color(processed_code)
                authors = process_author(processed_code)
                author_icons = process_author_icon(processed_code)
                author_urls = process_author_url(processed_code)
                images = process_image(processed_code)
                thumbnails = process_thumbnail(processed_code)
                title_urls = process_title_url(processed_code)

                # Enviar texto simple si existe
                if plain_text:
                    await ctx.channel.send(plain_text)

                # Crear y enviar los embeds combinados
                for indice, descripcion in descriptions.items():
                    embed = discord.Embed(description=descripcion)
                    if indice in titles:
                        embed.title = titles[indice]
                    if indice in title_urls:
                        embed.url = title_urls[indice]
                    if indice in colors:
                        embed.color = discord.Color(int(colors[indice][1:], 16))
                    if indice in authors:
                        embed.set_author(
                            name=authors[indice],
                            icon_url=author_icons.get(indice, None),
                            url=author_urls.get(indice, None)
                        )
                    if indice in images:
                        embed.set_image(url=images[indice])
                    if indice in thumbnails:
                        embed.set_thumbnail(url=thumbnails[indice])

                    await ctx.channel.send(embed=embed)

            else:
                await ctx.channel.send(f"❌ Tipo de comando no válido: {command_type}")

        except Exception as error:
            await handle_error(ctx, error)

    async def on_message(self, message):
        """
        Escucha todos los mensajes en el servidor y ejecuta los comandos $onMessage.
        """
        if message.author.bot:
            return  # Ignora mensajes de otros bots

        ctx = await self.bot.get_context(message)

        for command in self.on_message_commands:
            await self.execute_command(ctx, command['code'], "$onMessage", message.content)
