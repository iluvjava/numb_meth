"""
    Given a polynomial, we find its roots and the corresponding geometric multiplicity, high precision

------------------------------------------------------------------------------------------------------------------------
Algorithm:
------------------------------------------------------------------------------------------------------------------------
Basic idea:
    * Use Newton's method too look for the roots of the polynomials.
    * Use derivative to determine the repeated roots and them optimize it for accuracy.


"""

from core2 import *
from typing import Type, Dict
MyPolynomial = Type[Polynomial]


def solve(p: MyPolynomial, x0: Number = None) -> Dict[Number, int]:
    """
        Attempts to solve the polynomial at that point.
    :param p:
        The polynomial.
    :return:
        dict mappint the roots to it'ss multiplicity.
    """
    x0 = random() + (-1)**(0.5)*random() if x0 is None else x0
    TOL = 1e-5
    maxitr = 1e1

    k = 0
    # The kth derivative

    while k + 1 <= p._Deg:
        def g(point):
            res = p.eval_all(point, derv=k + 1)
            return point - res[k] / res[k + 1]

        # Start fixed point iteration.
        itr = 0
        x1 = g(x0)
        while abs(x1 - x0) > TOL and itr < maxitr:
            x0 = x1
            x1 = g(x1)
            itr += 1

        # Checking the fixed point iteration result for repeated roots.
        dgdx = (g(x1+1e-4) - g(x1))/1e-4
        if abs(dgdx) < 1e-2:
            return x0
        k += 1
        continue


if __name__ == "__main__":
    p = Polynomial([1, 2, 1])
    print(solve(p))

    p = Polynomial([1, 4, 6, 4, 1])
    print(solve(p))