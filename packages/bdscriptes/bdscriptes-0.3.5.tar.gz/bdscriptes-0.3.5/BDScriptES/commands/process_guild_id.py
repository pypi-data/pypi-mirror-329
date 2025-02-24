import re
import discord

async def process_guild_id(code, ctx):
    """
    Procesa la función $guildID.
    - Si se usa $guildID, retorna el ID del servidor actual.
    - Si se usa $guildID[nombre del servidor], retorna el ID del servidor con ese nombre.
    Maneja errores como:
    - $.. []: No se abrieron los corchetes.
    - $guildID[]: El argumento no puede estar vacío.
    - $guildID[hola]: El servidor no existe con el nombre proporcionado.
    """
    # Expresión regular para encontrar $guildID y $guildID[nombre]
    guild_id_pattern = re.compile(r'\$guildID(?:\[(.*?)\])?')

    def replace_guild_id(match):
        # Obtener el nombre del servidor (si existe)
        guild_name = match.group(1)

        if guild_name is None:
            # Caso: $guildID (sin corchetes)
            return str(ctx.guild.id) if ctx.guild else "Error: No estás en un servidor."
        else:
            # Caso: $guildID[nombre del servidor]
            if not guild_name.strip():
                return "Error: El argumento no puede estar vacío."

            # Buscar el servidor por nombre
            guild = discord.utils.get(ctx.bot.guilds, name=guild_name)
            if guild:
                return str(guild.id)
            else:
                return f"Error: El servidor '{guild_name}' no existe."

    # Reemplazar todas las coincidencias en el código
    processed_code = guild_id_pattern.sub(replace_guild_id, code)
    return processed_code