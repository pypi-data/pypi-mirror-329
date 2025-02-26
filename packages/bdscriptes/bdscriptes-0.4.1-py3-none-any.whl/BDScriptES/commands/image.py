def process_image(code):
    """
    Procesa los placeholders $image[url;(índice opcional)].
    Retorna un diccionario con las imágenes asociadas a los índices de embed.
    """
    images = {}
    start = 0

    while True:
        start_idx = code.find("$image[", start)
        if start_idx == -1:
            break

        if start_idx > 0 and code[start_idx - 1].isalnum():
            raise ValueError(f"❌ Invalid format: '{code[start_idx-1:start_idx+8]}...' (Expected '$imagen[...]')")

        end_idx = code.find("]", start_idx)
        if end_idx == -1:
            raise ValueError("❌ '$image[' not closed with ']'")

        placeholder = code[start_idx + len("$image["):end_idx]
        parts = placeholder.split(";")
        image_url = parts[0].strip()
        indice_embed = int(parts[1].strip()) if len(parts) > 1 else 1

        if not image_url:
            raise ValueError("❌ '$image[]' missing URL")

        images[indice_embed] = image_url
        start = end_idx + 1

    return images
