# process_message_user_id.py

def process_message_user_id(code, ctx):
    """
    Procesa la función $messageUserID.
    Reemplaza $messageUserID con el ID del usuario que ejecutó el comando.
    """
    if "$mensajeID" in code:
        code = code.replace("$messageUserID", str(ctx.author.id))
    return code