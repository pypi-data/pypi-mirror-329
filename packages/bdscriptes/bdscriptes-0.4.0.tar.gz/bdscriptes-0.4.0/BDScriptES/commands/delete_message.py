import discord

async def process_delete_message(code, ctx, bot):
    """
    Procesa la función $deleteMessage[channel_id;message_id].
    Elimina un mensaje específico en un canal específico y maneja errores correctamente.
    """
    while "$deleteMessage[" in code:
        start = code.find("$deleteMessage[") + len("$deleteMessage[")
        end = code.find("]", start)

        if end == -1:
            raise ValueError("❌ Error: Falta cerrar los corchetes en $deleteMessage.")

        params = code[start:end].split(";")

        if len(params) != 2:
            raise ValueError("❌ Error: Se requieren exactamente dos argumentos en $deleteMessage[channel_id;message_id].")

        channel_id, message_id = params

        if not channel_id.isdigit() or not message_id.isdigit():
            raise ValueError("❌ Error: Tanto channel_id como message_id deben ser números enteros válidos.")

        channel = bot.get_channel(int(channel_id))
        if channel is None:
            raise ValueError(f"❌ Error: El canal con ID {channel_id} no es válido o el bot no tiene acceso.")

        try:
            message = await channel.fetch_message(int(message_id))
            if message:
                await message.delete()
        except discord.NotFound:
            raise ValueError(f"❌ Error: No se encontró el mensaje con ID {message_id} en el canal {channel_id}.")
        except discord.Forbidden:
            raise ValueError("❌ Error: El bot no tiene permisos para eliminar mensajes en este canal.")
        except discord.HTTPException as e:
            raise ValueError(f"❌ Error de Discord: {e}")

        # Reemplazar solo la primera instancia de la función correctamente
        code = code[:start - len("$deleteMessage[")] + code[end + 1:]

    return code
