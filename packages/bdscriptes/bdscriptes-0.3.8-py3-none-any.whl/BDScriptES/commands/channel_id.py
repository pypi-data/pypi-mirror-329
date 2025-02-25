def process_channel_id(code, ctx):
    """
    Reemplaza $channelID con el ID del canal donde se ejecuta el comando.
    """
    return code.replace("$channelID", str(ctx.channel.id))