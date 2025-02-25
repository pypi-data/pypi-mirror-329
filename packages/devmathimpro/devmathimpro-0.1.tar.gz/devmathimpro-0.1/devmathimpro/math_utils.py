def factorial(n):
    """Вычисляет факториал числа n."""
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел.")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def is_prime(n):
    """Проверяет, является ли число n простым."""
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True