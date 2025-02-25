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
            raise ValueError(f"❌ '{left} {operador} {right}' is invalid, text can only use '==' or '!='")
    else:
        raise ValueError(f"❌ '{left} {operador} {right}' is invalid, cannot compare numbers with text")

    return eval(f"{repr(left)} {operador} {repr(right)}")

def validar_condicion(condition):
    if not condition:
        return "❌ '$if[]' comparison none not found"

    operador_encontrado = None
    for operador in OPERADORES_VALIDOS:
        if operador in condition:
            operador_encontrado = operador
            break

    if not operador_encontrado:
        return f"❌ '$if[{condition}]' is not valid, expected one of {OPERADORES_VALIDOS}"

    partes = condition.split(operador_encontrado)
    if len(partes) != 2 or not partes[0].strip() or not partes[1].strip():
        return f"❌ '$if[{condition}]' comparison not found, expected format like 'X {operador_encontrado} Y'"

    return None  # ✅ Condición válida

def process_conditions(code):
    lines = code.strip().split("\n")
    stack = []  
    result = []  
    ejecutar_else = True  

    for line in lines:
        line = line.strip()

        if line.startswith("$if[") or line.startswith("$elseif["):
            is_if = line.startswith("$if[")
            condition = line[4 if is_if else 8:-1].strip()
            error_msg = validar_condicion(condition)
            if error_msg:
                raise ValueError(error_msg)

            operador_encontrado = next((op for op in OPERADORES_VALIDOS if op in condition), None)
            left, right = condition.split(operador_encontrado)
            left, right = left.strip(), right.strip()
            condition_result = evaluate_condition(left, operador_encontrado, right)

            if is_if:
                stack.append({"executing": condition_result, "was_true": condition_result})
            else:
                if stack and condition_result:
                    stack[-1]["executing"] = True
                    stack[-1]["was_true"] = True

            if condition_result:
                
                ejecutar_else = False  

        elif line.startswith("$else"):
            if not stack:
                raise ValueError("❌ '$else' sin un '$if[...]' previo.")

            if ejecutar_else:
                stack[-1]["executing"] = True
                stack[-1]["was_true"] = True  

        elif line.startswith("$endif"):
            if not stack:
                raise ValueError("❌ '$endif' sin un '$if[...]' previo.")

            stack.pop()  

        elif stack and stack[-1]["executing"]:
            result.append(line)  

    if stack:
        raise ValueError("❌ Error: Falta '$endif' en alguna estructura.")

    return "\n".join(result)



