def process_author(code):
    """
    Procesa los placeholders $author[texto;(índice opcional)].
    Retorna un diccionario con los autores asociados a los índices de embed.
    """
    authors = {}
    start = 0

    while True:
        start_idx = code.find("$autor[", start)
        if start_idx == -1:
            break

        # 🔍 Verifica que el marcador empieza correctamente y no tiene caracteres adicionales
        if start_idx > 0 and code[start_idx - 1].isalnum():
            raise ValueError(f"❌ Invalid format: '{code[start_idx-1:start_idx+9]}...' (Expected '$autor[...]')")

        end_idx = code.find("]", start_idx)
        if end_idx == -1:
            raise ValueError("❌ '$autor[' not closed with ']'")

        placeholder = code[start_idx + len("$autor["):end_idx]
        parts = placeholder.split(";")
        author_text = parts[0].strip()
        indice_embed = int(parts[1].strip()) if len(parts) > 1 else 1

        if not author_text:
            raise ValueError("❌ '$autor[]' missing author text")

        authors[indice_embed] = author_text
        start = end_idx + 1

    return authors
