def process_message(code, message_content):
    """
    Procesa los placeholders $message, $message[N] pero ignora $deletecommand sin eliminarlo.
    
    Parámetros:
    - code (str): El código que contiene los placeholders.
    - message_content (str): El contenido del mensaje del usuario.
    
    Retorna:
    - str: Código procesado donde $deletecommand sigue existiendo, pero sin ser ejecutado.
    """
    words = message_content.split()  # Divide el mensaje en palabras

    start = 0
    while True:
        start_idx = code.find("$message", start)
        if start_idx == -1:
            break  # No hay más placeholders

        end_idx = code.find("]", start_idx)
        
        if "[" in code[start_idx:]:  # Se abrió '[' pero...
            if end_idx == -1:
                raise ValueError("❌ '$message[' not closed with ']'")  # Falta cerrar
            elif end_idx == start_idx + len("$message["):  # Caso de $message[]
                raise ValueError("❌ '$message[]' index is empty")  # Índice vacío

        # Extrae el índice si existe
        placeholder = code[start_idx + len("$message"):end_idx + 1] if end_idx != -1 else "$message"
        index_part = placeholder[1:-1] if placeholder.startswith("[") and placeholder.endswith("]") else None

        if index_part is None:
            replacement = message_content  # $message → retorna todo el mensaje
        else:
            if not index_part.isdigit():
                raise ValueError(f"❌ Invalid index in '$message[{index_part}]' (Expected a number)")  # Índice inválido
            
            index = int(index_part) - 1  # Convertimos a entero (1-based index)
            replacement = words[index] if 0 <= index < len(words) else ""  # Retorna palabra o vacío si el índice no existe

        # Reemplaza el placeholder por su valor correspondiente
        code = code[:start_idx] + replacement + code[end_idx + 1:] if end_idx != -1 else code[:start_idx] + replacement

        # Avanza la búsqueda
        start = start_idx + len(replacement)

    return code  # Devuelve el código con $deletecommand intacto
