from expr import parseExpression, simplifyExpression, flatten_add

def solveEquation(expression):
    parts = expression.split('=')
    if len(parts) != 2:
        raise ValueError("Did you know that an equation has exactly one equal sign? I didn't either.")
    left = parseExpression(parts[0])
    right = parseExpression(parts[1])
    equalsZeroForm = ("subtract", left, right)
    equalsZeroForm = simplifyExpression(equalsZeroForm)
    terms = flatten_add(equalsZeroForm)
    exponent = 1
    for term in terms:
        if isinstance(term, tuple):
            operator, left, right = term
            if operator == "power" and right == 2:
                exponent = 2
            elif operator == "multiply" and (left == ("power", "x", 2) or right == ("power", "x", 2)):
                exponent = 2

    if exponent == 1:
        return solveLinear(terms)
    elif exponent == 2:
        return solveQuadratic(terms)
    else:
        raise ValueError("Sir, I don't know how to handle this. My professor never taught me how to handle a cubic or higher.")


def solveLinear(terms):
    m = 0
    b = 0
    for term in terms:
        if isinstance(term, (int, float)):
            b += term
        elif term == "x":
            m += 1
        elif isinstance(term, tuple):
            operator, left, right = term
            if operator == "multiply" and isinstance(left, (int, float)) and right == "x": 
                m += left
            else:
                raise ValueError("I hate quadratic equations. In fact, I hate anything that isn't linear. Who am I?")

    if m == 0 and b == 0:
        return "Infinite solutions"
    elif m == 0 and b != 0:
        return "No solution"
    else:
        solution = (0 - b) / m
        if solution == 0:
            solution = 0
        return f"x = {solution}"

def solveQuadratic(terms):
    a = 0
    b = 0
    c = 0
    for term in terms:
        if isinstance(term, (int, float)):
            c += term
        elif term == 'x':
            b += 1
        elif term == ("power", "x", 2):
            a += 1
        elif isinstance(term, tuple):
            operator, left, right = term
            if operator == "multiply":
                if isinstance(left, (int, float)) and right == 'x':
                    b += left
                elif isinstance(left, (int, float)) and right == ("power", "x", 2):
                    a += left
    if a == 0:
        return solveLinear(terms)

    discriminant = (b ** 2) - (4 * a * c)
    if discriminant > 0:
        root1 = (-b + (discriminant ** 0.5)) / (2 * a)
        root2 = (-b - (discriminant ** 0.5)) / (2 * a)
        return f"x = {root1}, {root2}"
    elif discriminant == 0:
        root = -b / (2 * a)
        return f"x = {root}"
    elif discriminant < 0:
        real = -b / (2 * a) 
        imag = ((-discriminant) ** 0.5) / (2 * a)
        return f"x = {real} + {imag}i, {real} - {imag}i"


print(solveEquation("3x^2 = 12"))



    