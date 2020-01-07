
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
        compute the value of (n + 1)(n + 2)...(m)
        spacial cases:
            * m - n == 1
                return m
            * m - n == 0
                return 1
    :param n:
        non negative integer.
    :param m:
        a positive integer
    :return:
        the result
    """
    assert n <= m and m > 0 and n > 0, "m, n must be possitive and m should be larger than n "
    running_Prod = 1
    for i in range(n + 1, m):
        running_Prod *= i
    return running_Prod


def firstorder_5thdeg_finitediff(fxn, mid_Point, h=1e-4):
    """
        Given 3 points and the function, the interval is optional,
        it will return the derivative of the function centered at that point.
    :param fxn:
        A function.
    :param mid_Point:
        The mid point of the funciton.
    :return:
        The derivative around the mid_point.
    """
    c = [1, -8, 0, 8, -1]
    pass
