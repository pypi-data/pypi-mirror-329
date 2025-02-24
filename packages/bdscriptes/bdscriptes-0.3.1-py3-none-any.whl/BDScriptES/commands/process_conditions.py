import re

# Lista de operadores válidos
OPERADORES_VALIDOS = {">", "<", ">=", "<=", "!=", "=="}

def es_numero(valor):
    """
    Verifica si el valor es un número (entero o decimal).
    """
    try:
        float(valor)
        return True
    except ValueError:
        return False

def evaluate_condition(left, operador, right):
    """
    Evalúa una condición, asegurando que solo se usen operadores válidos y respetando el tipo de datos.
    """
    if es_numero(left) and es_numero(right):
        # Comparación numérica
        left, right = float(left), float(right)
    elif not es_numero(left) and not es_numero(right):
        # Comparación de texto, pero solo permite "==" y "!="
        if operador not in {"==", "!="}:
            raise ValueError(f"❌ '{left} {operador} {right}' is invalid, text can only use '==' or '!='")
    else:
        # Error: Mezcla de texto y número
        raise ValueError(f"❌ '{left} {operador} {right}' is invalid, cannot compare numbers with text")

    # Evaluar la condición
    return eval(f"{repr(left)} {operador} {repr(right)}")

def validar_condicion(condition):
    """
    Valida que la condición tenga un operador válido y tenga el formato correcto.
    Retorna un mensaje de error si la condición es inválida.
    """
    if not condition:
        return "❌ '$if[]' comparison none not found"

    # Verificar si la condición contiene un operador válido
    operador_encontrado = None
    for operador in OPERADORES_VALIDOS:
        if operador in condition:
            operador_encontrado = operador
            break

    if not operador_encontrado:
        return f"❌ '$if[{condition}]' is not valid, expected one of {OPERADORES_VALIDOS}"

    # Dividir la condición en partes izquierda y derecha
    partes = condition.split(operador_encontrado)
    if len(partes) != 2 or not partes[0].strip() or not partes[1].strip():
        return f"❌ '$if[{condition}]' comparison not found, expected format like 'X {operador_encontrado} Y'"

    return None  # ✅ Condición válida

def process_conditions(code):
    """
    Procesa los bloques condicionales $if, $else y $endif con validación de errores.
    """
    while '$if[' in code:
        condition_pattern = re.compile(r'(\$if\[(.*?)\])(.*?)($else(.*?))?\$endif', re.DOTALL)

        def replace_condition(match):
            full_if = match.group(1)  # "$if[...]"
            condition = match.group(2).strip()  # La condición dentro de "[...]"
            content = match.group(3).strip()  # Contenido dentro del if
            else_block = match.group(5).strip() if match.group(4) else ""  # Bloque else si existe

            # 📌 Validar la condición
            error_msg = validar_condicion(condition)
            if error_msg:
                raise ValueError(error_msg)

            # ✅ Evaluar condición
            operador_encontrado = None
            for operador in OPERADORES_VALIDOS:
                if operador in condition:
                    operador_encontrado = operador
                    break

            left, right = condition.split(operador_encontrado)
            left, right = left.strip(), right.strip()

            if evaluate_condition(left, operador_encontrado, right):
                return content.strip()
            else:
                return else_block.strip()

        # 📌 Validar si hay un `$if[` sin su `$endif`
        if "$if[" in code and "$endif" not in code:
            raise ValueError("❌ '$if[...]' error, missing $endif")

        code = condition_pattern.sub(replace_condition, code)

    return code
