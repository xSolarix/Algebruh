test = ("power", "x", 2)
test2 = ("add", ("multiply", 4, "x"), ("add", 2, 3))

def evaluateExpression(expression, variables):
    if isinstance(expression, (int, float)):
        return expression
    
    if isinstance(expression, str):
        return variables[expression]
    
    operation, num1, num2 = expression
    result = 0
    if operation == "add":
        result = evaluateExpression(num1, variables) + evaluateExpression(num2, variables)
    elif operation == "subtract":
        result = evaluateExpression(num1, variables) - evaluateExpression(num2, variables)
    elif operation == "multiply":
        result = evaluateExpression(num1, variables) * evaluateExpression(num2, variables)
    elif operation == "divide":
        result = evaluateExpression(num1, variables) / evaluateExpression(num2, variables)
    elif operation == "power":
        result = evaluateExpression(num1, variables) ** evaluateExpression(num2, variables)
    else:
        result = 0
    return result

def flatten_add(expression):
    if isinstance(expression, (int, float, str)):
        return [expression]
    operation, left, right = expression

    if operation == "add":
        return flatten_add(left) + flatten_add(right)
    else:
        return [expression]

def simplifyExpression(expression):
    if isinstance(expression, (int, float, str)):
        return expression

    operation, left, right = expression

    if operation == "subtract":
        return simplifyExpression(("add", left, ("multiply", -1, right)))

    left = simplifyExpression(left)
    right = simplifyExpression(right)

    if operation == "add":
        terms = flatten_add(("add", left, right))

        constant_sum = 0
        term_totals = {}

        for term in terms:
            if isinstance(term, (int, float)):
                constant_sum += term
            elif isinstance(term, tuple) and term[0] == "multiply":
                _, m_left, m_right = term
                if isinstance(m_left, (int, float)):
                    coeff, base = m_left, m_right
                elif isinstance(m_right, (int, float)):
                    coeff, base = m_right, m_left
                else:
                    coeff, base = 1, term
                term_totals[base] = term_totals.get(base, 0) + coeff
            else:
                term_totals[term] = term_totals.get(term, 0) + 1

        surviving = []
        if constant_sum != 0:
            surviving.append(constant_sum)

        for base, coeff in term_totals.items():
            if coeff == 0:
                continue
            elif coeff == 1:
                surviving.append(base)
            else:
                surviving.append(simplifyExpression(("multiply", coeff, base)))

        if len(surviving) == 0:
            return 0
        result = surviving[0]
        for item in surviving[1:]:
            result = ("add", result, item)
        return result

    elif operation == "multiply":
        if left == 0 or right == 0:
            return 0
        elif left == 1:
            return right
        elif right == 1:
            return left
        elif isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left * right
        elif isinstance(left, (int, float)) and isinstance(right, tuple) and right[0] == "multiply":
            _, inner_left, inner_right = right
            if isinstance(inner_left, (int, float)):
                return simplifyExpression(("multiply", left * inner_left, inner_right))
            elif isinstance(inner_right, (int, float)):
                return simplifyExpression(("multiply", left * inner_right, inner_left))
        elif isinstance(right, (int, float)) and isinstance(left, tuple) and left[0] == "multiply":
            _, inner_left, inner_right = left
            if isinstance(inner_left, (int, float)):
                return simplifyExpression(("multiply", right * inner_left, inner_right))
            elif isinstance(inner_right, (int, float)):
                return simplifyExpression(("multiply", right * inner_right, inner_left))
            
    elif operation == "divide":
        if right == 0:
            raise ZeroDivisionError("Cannot Divide By Zero (limits, anyone?)")
        elif left == 0:
            return 0
        elif left == right:
            return 1
        else:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left / right
    elif operation == "power":
        if right == 0:
            return 1
        elif left == 0:
            return 0
        elif left == 1:
            return 1
        elif right == 1:
            return left
        else:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left ** right

    return (operation, left, right)

def beautifyExpression(expression): # Aren't tuples beautiful enough already?
    if isinstance(expression, (int, float, str)):
        return str(expression)

    operation, left, right = expression

    if operation == "multiply":
        if isinstance(left, (int, float)) and isinstance(right, str):
            return f"{left}{right}"
        elif isinstance(left, (int, float)) and isinstance(right, tuple) and right[0] == "power" and isinstance(right[1], str):
            return f"{left}{beautifyExpression(right)}"

    left_str = beautifyExpression(left)
    right_str = beautifyExpression(right)

    if operation == "add":
        return f"({left_str} + {right_str})"
    elif operation == "subtract":
        return f"({left_str} - {right_str})"
    elif operation == "multiply":
        return f"({left_str} * {right_str})"
    elif operation == "divide":
        return f"({left_str} / {right_str})"
    elif operation == "power":
        return f"{left_str}^{right_str}"

def tokenizeExpression(text):
    tokens = []
    i = 0

    while i < len(text):
        char = text[i]
        if char == " ":
            i += 1

        elif char.isdigit():
            num_str = ""
            while i < len(text) and (text[i].isdigit() or text[i] == "."):
                num_str += text[i]
                i += 1
            tokens.append(float(num_str) if "." in num_str else int(num_str))

        elif char.isalpha():
            tokens.append(char)
            i += 1

        else:
            if char in "+-*/^()":
                is_unary = (len(tokens) == 0) or (tokens[-1] in ["(", "+", "-", "*", "/", "^"])
                if char == "-" and is_unary:
                    tokens.append(-1)
                    tokens.append("*")
                    i += 1
                elif char == "+" and is_unary:
                    i += 1
                else:
                    tokens.append(char)
                    i += 1
            else:
                raise ValueError("Uhh...is " + char + " really supposed to be there? I think not.")

    final_tokens = []
    for j in range(len(tokens)):
        curr = tokens[j]
        final_tokens.append(curr)

        if j + 1 < len(tokens):
            nxt = tokens[j + 1]
            left_ok = isinstance(curr, (int, float)) or (isinstance(curr, str) and curr.isalpha()) or curr == ")"
            right_ok = (isinstance(nxt, str) and nxt.isalpha()) or nxt == "("

            if left_ok and right_ok:
                final_tokens.append("*")

    return final_tokens

def parseExpression(text):
    tokens = tokenizeExpression(text)
    output = []
    operators = []
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
    operationNames = {"+": "add", "-": "subtract", "*": "multiply", "/": "divide", "^": "power"}

    for token in tokens:
        if isinstance(token, (int, float)) or (isinstance(token, str) and token.isalpha()):
            output.append(token)
        elif token == "(":
            operators.append("(")
        elif token == ")":
            while len(operators) > 0 and operators[-1] != "(":
                op = operators.pop()
                right = output.pop()
                left = output.pop()
                output.append((operationNames[op], left, right))
            operators.pop()
        elif token in precedence:
            while len(operators) > 0 and operators[-1] != "(":
                if token == "^":
                    if not (precedence[operators[-1]] > precedence[token]):
                        break
                else:
                    if not (precedence[operators[-1]] >= precedence[token]):
                        break

                op = operators.pop()
                right = output.pop()
                left = output.pop()
                output.append((operationNames[op], left, right))
            operators.append(token)

    while len(operators) > 0:
        op = operators.pop()
        right = output.pop()
        left = output.pop()
        output.append((operationNames[op], left, right))

    return output[0]
