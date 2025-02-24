
from .process_title import process_title
from .process_description import process_description
from .process_color import process_color
from .process_author import process_author
from .process_author_icon import process_author_icon
from .process_author_url import process_author_url
from .process_image import process_image
from .process_thumbnail import process_thumbnail
from .process_title_url import process_title_url



from .process_conditions import process_conditions
from .process_var import procesar_variables


from BDScriptES.utils.process_text import process_text
from BDScriptES.utils.error_handler import handle_error  # Importamos el manejador de errores

import discord

class CommandHandler:
    def __init__(self, bot):
        self.bot = bot
        self.commands_dict = {}

    def new_command(self, name, type, code):
        """
        Registra un nuevo comando.
        """
        self.commands_dict[name] = {'type': type, 'code': code}

        # Crear un comando dinámico usando discord.ext.commands
        @self.bot.command(name=name)
        async def dynamic_command(ctx):
            try:
                code = self.commands_dict[name]['code']
                command_type = self.commands_dict[name]['type']

                # Procesar variables primero
                processed_code = procesar_variables(code)

                # Procesar condiciones
                processed_code = process_conditions(processed_code)

                # Validar el tipo de comando
                if command_type == "send":
                    # Procesar títulos y descripciones (con validación de errores)
                    
                    titles = process_title(processed_code)
                    descriptions = process_description(processed_code)  
                    colors = process_color(processed_code)  
                    authors = process_author(processed_code)
                    author_icons = process_author_icon(processed_code)
                    author_urls = process_author_url(processed_code)
                    images = process_image(processed_code)
                    thumbnails = process_thumbnail(processed_code)
                    title_urls = process_title_url(processed_code)


                    # Extraer texto fuera de los marcadores $description y $title
                    plain_text = process_text(processed_code)

                    # Enviar texto simple si existe
                    if plain_text:
                        await ctx.send(plain_text)

                    # Crear y enviar los embeds combinados
                    for indice, descripcion in descriptions.items():
                        embed = discord.Embed(description=descripcion)
                        if indice in titles:
                            embed.title = titles[indice]

                        if indice in title_urls:
                            embed.url = title_urls[indice]

                        if indice in colors:
                            embed.color = discord.Color(int(colors[indice][1:], 16))  # Convertir hex a decimal

                        
                        if indice in authors:
                            embed.set_author(
                                name=authors[indice],
                                icon_url=author_icons.get(indice, None),  # Si no hay icono, usa Embed.Empty
                                url=author_urls.get(indice, None)  # Si no hay URL, usa Embed.Empty
                                )
                        
                        if indice in images:
                            embed.set_image(url=images[indice])  # Asignar imagen si existe

                        if indice in thumbnails:
                            embed.set_thumbnail(url=thumbnails[indice])  # Asignar thumbnail si existe

                            

                        await ctx.send(embed=embed)
                else:
                    await ctx.send(f"❌ Tipo de comando no válido: {command_type}")

            except Exception as error:
                await handle_error(ctx, error)  # Capturar y manejar el error
