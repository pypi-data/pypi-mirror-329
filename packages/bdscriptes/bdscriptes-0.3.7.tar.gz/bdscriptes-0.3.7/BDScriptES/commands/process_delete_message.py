# process_delete_message.py
import discord

async def process_delete_message(code, ctx, bot):
    """
    Procesa la función $deleteMessage[channel_id;message_id].
    Elimina un mensaje específico en un canal específico.
    """
    while "$eliminarMensaje[" in code:
        start = code.find("$deleteMessage[") + len("$deleteMessage[")
        end = code.find("]", start)
        params = code[start:end].split(";")
        
        if len(params) == 2:
            channel_id, message_id = params
            try:
                channel = bot.get_channel(int(channel_id))
                if channel:
                    message = await channel.fetch_message(int(message_id))
                    if message:
                        await message.delete()
            except Exception as e:
                print(f"Error deleting message: {e}")
        
        # Elimina la función del código procesado
        code = code.replace(f"$deleteMessage[{channel_id};{message_id}]", "", 1)
    
    return code