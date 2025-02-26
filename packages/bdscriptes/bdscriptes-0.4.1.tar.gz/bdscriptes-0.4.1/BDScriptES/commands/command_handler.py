from .title import process_title
from .description import process_description
from .color import process_color
from .author import process_author
from .author_icon import process_author_icon
from .author_url import process_author_url
from .image import process_image
from .thumbnail import process_thumbnail
from .title_url import process_title_url
from .message import process_message
from .condicion import process_conditions
from .var import procesar_variables
from .delete_message import process_delete_message
from .message_user_id import process_message_user_id
from .guild_id import process_guild_id
from BDScriptES.utils.process_text import process_text
from BDScriptES.utils.error_handler import handle_error
from .channel_id import process_channel_id
from .loop import process_loops





import discord

class CommandHandler:
    def __init__(self, bot):
        self.bot = bot
        self.commands_dict = {}
        self.events_dict = {}  # Diccionario para almacenar eventos

    def new_command(self, name, type, code):
        """
        Registra un nuevo comando.
        """
        self.commands_dict[name] = {'type': type, 'code': code}

        @self.bot.command(name=name)
        async def dynamic_command(ctx):
            try:
                code = self.commands_dict[name]['code']
                command_type = self.commands_dict[name]['type']

                message_content = ctx.message.content[len(ctx.prefix) + len(ctx.command.name) + 1:].strip()

                
                


                
                # Procesar variables en el código
                
                processed_code = await process_guild_id(code, ctx)
                print("guild:", processed_code)

                processed_code = process_message_user_id(processed_code, ctx)
                print("message user id:", processed_code)

                processed_code = process_message(processed_code, message_content)
                print("process message:", processed_code)

                processed_code = process_channel_id(processed_code, ctx)  # Agregar aquí
                print("channelid", processed_code)

                processed_code = procesar_variables(processed_code)
                print("variables", processed_code)

                
                

                processed_code = process_conditions(processed_code)
                print("conditions", processed_code)

                processed_code = process_loops(processed_code, None)
                print("loops:", processed_code)
                

                

                processed_code = await process_delete_message(processed_code, ctx, self.bot)
                
                plain_text = process_text(processed_code)

                print("plain text", processed_code)

                

                


                if command_type == "$sendMessage":
                    # Procesar funciones de embed
                    titles = process_title(processed_code)
                    
                    descriptions = process_description(processed_code)
                    colors = process_color(processed_code)
                    authors = process_author(processed_code)
                    author_icons = process_author_icon(processed_code)
                    author_urls = process_author_url(processed_code)
                    images = process_image(processed_code)
                    thumbnails = process_thumbnail(processed_code)
                    title_urls = process_title_url(processed_code)

                    

                    if plain_text:
                        await ctx.send(plain_text)

                    # Crear y enviar los embeds
            # Crear y enviar los embeds
                    embed_indices = set(titles.keys()) | set(title_urls.keys()) | set(colors.keys()) | \
                    set(authors.keys()) | set(author_icons.keys()) | set(author_urls.keys()) | \
                    set(images.keys()) | set(thumbnails.keys()) | set(descriptions.keys())

                    for indice in embed_indices:
    # Crear embed solo si hay al menos una propiedad
                        embed = discord.Embed()

                        if indice in descriptions:
                            embed.description = descriptions[indice]
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

                        await ctx.send(embed=embed)


                else:
                    await ctx.send(f"❌ Tipo de comando no válido: {command_type}")

            except Exception as error:
                await handle_error(ctx, error)

    def new_event(self, type, code):
        """
        Registra un nuevo evento.
        """
        self.events_dict[type] = code

        if type == "$onMessage":
            @self.bot.event
            async def on_message(message):
                # Ignorar mensajes de otros bots (incluido el propio bot)
                if message.author.bot:
                    return

                ctx = await self.bot.get_context(message)

                # Ejecutar el código del evento
                await self.execute_code(ctx, code, message_content=message.content)

                # Permitir que el bot siga procesando comandos
                await self.bot.process_commands(message)

    async def execute_code(self, ctx, code, message_content=""):
        """
        Ejecuta el código del evento o comando.
        """
        try:
            
         
            processed_code = await process_guild_id(code, ctx)
            processed_code = process_message_user_id(processed_code, ctx)
            processed_code = process_message(processed_code, message_content)
            processed_code = process_channel_id(processed_code, ctx)  # Agregar aquí
            processed_code = procesar_variables(processed_code)

           
            processed_code = process_conditions(processed_code)


            processed_code = process_loops(processed_code, None)
           

            processed_code = await process_delete_message(processed_code, ctx, self.bot)
            plain_text = process_text(processed_code)

            
            # Procesar funciones de embed
            titles = process_title(processed_code)
            descriptions = process_description(processed_code)
            colors = process_color(processed_code)
            authors = process_author(processed_code)
            author_icons = process_author_icon(processed_code)
            author_urls = process_author_url(processed_code)
            images = process_image(processed_code)
            thumbnails = process_thumbnail(processed_code)
            title_urls = process_title_url(processed_code)


            

            if plain_text:
                await ctx.send(plain_text)

            # Crear y enviar los embeds
            embed_indices = set(titles.keys()) | set(title_urls.keys()) | set(colors.keys()) | \
                set(authors.keys()) | set(author_icons.keys()) | set(author_urls.keys()) | \
                set(images.keys()) | set(thumbnails.keys()) | set(descriptions.keys())

            for indice in embed_indices:
    # Crear embed solo si hay al menos una propiedad
                embed = discord.Embed()

                if indice in descriptions:
                   embed.description = descriptions[indice]
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

                await ctx.send(embed=embed)


        except Exception as error:
            await handle_error(ctx, error)
