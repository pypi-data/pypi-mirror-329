OPERADORES_VALIDOS = {">", "<", ">=", "<=", "!=", "=="}

def es_numero(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False

def evaluate_condition(left, operador, right):
    if es_numero(left) and es_numero(right):
        left, right = float(left), float(right)
    elif not es_numero(left) and not es_numero(right):
        if operador not in {"==", "!="}:
            raise ValueError(f"❌ '{left} {operador} {right}' no es válido, solo se permite '==' o '!=' para texto.")
    else:
        raise ValueError(f"❌ '{left} {operador} {right}' no es válido, no se pueden comparar números con texto.")

    return eval(f"{repr(left)} {operador} {repr(right)}")

def extraer_condicion(line):
    if line.startswith("$if[") or line.startswith("$elseif["):
        inicio = 4 if line.startswith("$if[") else 8
        if not line.endswith("]"):
            raise ValueError(f"❌ Condición mal formada en: {line}")
        return line[inicio:-1].strip()
    return None

def process_conditions(code):
    if not any(tag in code for tag in ["$if[", "$elseif[", "$else", "$endif"]):  
        return code.strip()

    lines = code.split("\n")
    result = []
    stack = []  # Guarda estados de ejecución de los bloques

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("$if[") or line.startswith("$elseif["):
            is_if = line.startswith("$if[")
            condition = extraer_condicion(line)
            operador_encontrado = next(op for op in OPERADORES_VALIDOS if op in condition)
            left, right = condition.split(operador_encontrado)
            left, right = left.strip(), right.strip()
            condition_result = evaluate_condition(left, operador_encontrado, right)

            if is_if:
                stack.append({"executing": condition_result})  
            else:
                if not stack:
                    raise ValueError("❌ '$elseif[...]' sin un '$if[...]' previo.")
                stack[-1]["executing"] = condition_result  

        elif line.startswith("$else"):
            if not stack:
                raise ValueError("❌ '$else' sin un '$if[...]' previo.")
            stack[-1]["executing"] = not stack[-1]["executing"]

        elif line.startswith("$endif"):
            if not stack:
                raise ValueError("❌ '$endif' sin un '$if[...]' previo.")
            stack.pop()

        elif stack and stack[-1]["executing"]:
            result.append(line)

    if stack:
        raise ValueError("❌ Falta '$endif' en alguna estructura.")

    return "\n".join(result)

 # Fixed
