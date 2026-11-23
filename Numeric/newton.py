function = "x**3 - 5*x**2 - 4*x + 2"
min_x = -1
max_x = 6

def get_derivative(func: str) -> str:
    import re
    derivative = ""
    for match in re.finditer(r"(?:([+-])\s*(\d*)\s*\*\s*)?x\*\*(-?\d+)", func):
        sign = match.group(1)
        coeff = match.group(2)
        power = match.group(3)
        if not sign or sign == "":
            sign = "+"
        if not coeff or coeff == "":
            coeff = "1"

        new_coeff = str(int(coeff) * int(power))
        new_power = str(int(power) - 1)
        derivative += f"{sign} {new_coeff}*x**{new_power} "

    for match in re.finditer(r"(?:([+-])\s*(\d*)\s*\*\s*)?x[^\*]", func):
        sign = match.group(1)
        coeff = match.group(2)
        if not sign or sign == "":
            sign = "+"
        if not coeff or coeff == "":
            coeff = "1"

        new_coeff = str(int(coeff))
        derivative += f"{sign} {new_coeff} "

    return derivative.strip()

def calculate(func: str, x_value: float) -> float:
    return eval(func.replace("x", str(x_value)))

def newton_method(func: str, derivate: str, initial_guess: float):
    x = initial_guess
    for _ in range(100):
        f_x = calculate(func, x)
        f_prime_x = calculate(derivate, x)        
        x = x - f_x / f_prime_x
    return x

def get_initial_guess(func: str, min_x, max_x, step=0.1):
    x_guess = (min_x + max_x) / 2 
    f_x_guess = calculate(func, x_guess)
    x = min_x
    while x <= max_x:
        f_x = calculate(func, x)
        if abs(f_x) < abs(f_x_guess):
            f_x_guess = f_x
            x_guess = x
        x += step
    return x_guess


if __name__ == "__main__":
    derivate  = get_derivative(function)
    print(f"Derivative: {derivate}")
    initial_guess = get_initial_guess(function, min_x, max_x)
    print(f"Initial guess: {initial_guess}")
    root = newton_method(function, derivate, 3)
    print(f"Root found: {root}")