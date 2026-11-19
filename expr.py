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

def simplifyExpression(expression):
    if isinstance(expression, (int, float, str)):
            return expression

    operation, left, right = expression
    left = simplifyExpression(left)
    right = simplifyExpression(right)

  
    if operation == "add":
        if left == 0:
            return right
        elif right == 0:
            return left
        else:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
    elif operation == "multiply":
        if left == 0:
            return 0
        elif right == 0:
            return 0
        elif left == 1:
            return right
        elif right == 1:
            return left
        else:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left * right
    elif operation == "subtract":
        if right == 0:
            return left
        elif left == right:
            return 0
        else:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left - right
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
        if left == 0:
            return 0
        elif left == 1:
            return 1
        elif right == 0:
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

        

print(beautifyExpression(("add", 3, ("multiply", 4, "x"))))
