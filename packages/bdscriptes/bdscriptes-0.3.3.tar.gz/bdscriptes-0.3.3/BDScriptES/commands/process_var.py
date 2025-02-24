def procesar_variables(codigo):
    texto = codigo
    variables = {}

    while "$var[" in texto:
        inicio = texto.find("$var[")  # Encuentra el primer $var[
        contador = 1
        fin = inicio + 5  # Saltamos "$var[" para buscar el cierre correcto

        # Buscar el cierre correcto del último `]`
        while fin < len(texto) and contador > 0:
            if texto[fin:fin + 5] == "$var[":  
                contador += 1  # Se encontró otro $var[, aumentamos el contador
            elif texto[fin] == "]":  
                contador -= 1  # Se encontró un cierre, reducimos el contador
            fin += 1

        if contador > 0:  # Si no encontró el cierre, salir del bucle
            break

        contenido = texto[inicio + 5:fin - 1]  # Obtener el contenido entre `$var[` y `]`
        partes = contenido.split(";", 1)  # Dividir en nombre y valor

        if len(partes) == 2:  # Definición de variable ($var[nombre;valor])
            nombre, valor = partes
            variables[nombre] = valor
            texto = texto[:inicio] + texto[fin:]  # Eliminar la definición del texto
        elif len(partes) == 1:  # Llamada a una variable ($var[nombre])
            nombre = partes[0]
            valor = variables.get(nombre, "")  # Si no existe, retornar vacío en lugar de quedarse cargando
            texto = texto[:inicio] + valor + texto[fin:]  # Reemplazar la variable en el texto

    return texto.strip()
