import re

def process_description(code):
    """
    Procesa el código y extrae los placeholders $description[texto;(índice embed)].
    Maneja errores de formato incorrecto.
    """
    descriptions = {}
    start = 0

    # 1️⃣ Verificar si hay "$description [" (con espacio antes de "[")
    if re.search(r"\$description\s+\[", code):
        raise ValueError("❌ '$description [' not opened correctly, remove spaces before '['")

    while True:
        # 2️⃣ Buscar el inicio de un placeholder válido
        start_idx = code.find("$description[", start)
        if start_idx == -1:
            break

        # 3️⃣ Buscar el cierre "]"
        end_idx = code.find("]", start_idx)
        if end_idx == -1:
            raise ValueError(f"❌ '{code[start_idx:]}' not close ] $description")  # Falta cierre ]

        # 4️⃣ Extraer el contenido dentro de los corchetes
        placeholder = code[start_idx + len("$description["):end_idx].strip()

        # 5️⃣ Validar errores específicos
        if placeholder == "":
            raise ValueError("❌ '$description []' no arguments")  # Placeholder vacío
        if ";" not in placeholder and placeholder.strip() == "":
            raise ValueError("❌ '$description[]' none text in 1 argument")  # Falta texto

        # 6️⃣ Dividir el contenido en texto y opcionalmente índice
        parts = placeholder.split(";")
        texto = parts[0].strip()  # El texto siempre está presente
        if not texto:
            raise ValueError("❌ '$description[]' none text in 1 argument")  # Texto vacío
        
        indice_embed = int(parts[1].strip()) if len(parts) > 1 else 1  # Índice predeterminado: 1

        # 7️⃣ Guardar en el diccionario
        descriptions[indice_embed] = texto

        # 8️⃣ Actualizar la posición de búsqueda
        start = end_idx + 1

    return descriptions
