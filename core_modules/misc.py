
__all__ = ["trunc_err_detect", "factorial", "partial_factorial"]


def trunc_err_detect(a, b):
    return a + b == max(a, b)


def factorial(n:int):
    """
        Compute the factorial of a non negative integer.
    :return:
        n!
    """
    assert n >= 0, f"Cannot take the factorial of the number: {n}"
    if n == 0:
        return 1
    return n*factorial(n - 1)

def partial_factorial(n:int, m:int):
    """
        compute the value of (n)(n + 1)(n + 2)...(m)
    :param n:
        non negative integer.
    :param m:
        a positive integer
    :return:
        the result
    """
    assert n <= m and m > 0 and n > 0, "m, n must be possitive and m should be larger than n "
    running_Prod = n
    for i in range(n + 1, m + 1):
        running_Prod *= i
    return running_Prod

