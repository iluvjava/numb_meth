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

def find_root(p: MyPolynomial, x0: Number = None):
    """
        Attempts to solve the polynomial at that point.
    :param p:
        The polynomial.
    :return:
        dict mappint the roots to it'ss multiplicity.
    """
    x0 = random() + (-1)**(0.5)*random() if x0 is None else x0
    TOL = 1e-10
    maxitr = 1e2

    k = 0
    # The kth derivative

    while k + 1 <= p._Deg:
        def g(point):
            res = p.eval_all(point, derv=k + 1)
            return point - (res[k] / res[k + 1])

        # Start fixed point iteration.
        itr = 0
        x1 = g(x0)
        while abs(x0 - x1) > TOL and itr < maxitr:
            x0 = x1
            x1 = g(x1)
            itr += 1

        # Checking the fixed point function result for repeated roots.
        dgdx = (g(x1+1e-4) - g(x1))/1e-4
        if abs(dgdx) < 1e-2:
            return x0, k + 1
        k += 1
        continue

    return None


def find_roots(p: MyPolynomial, results = None):
    results = results if results is not None else {}

    if p.deg() == 0:
        return results

    root, multiplicity = find_root(p)
    results[root] = multiplicity
    p = p.factor_out(root, multiplicity=multiplicity, poly=True)
    return find_roots(p, results)



if __name__ == "__main__":
    p = Polynomial([1, 2, 1])
    print(find_root(p))

    p = Polynomial([1, 4, 6, 4, 1])
    print(find_root(p))

    p = Polynomial([1, 5, 10, 10, 5, 1])
    print(find_root(p))

    p = Polynomial([1, -9, 33, -63, 66, -36, 8])
    print(f"Let's try on a hard one: {p}")
    root = find_root(p)
    print(f"This is one of the root with multiplicity: f{root}")
    print("Try to factor it out: ")
    p = p.factor_out(root[0], poly=True, multiplicity=root[1])
    print(p)
    print("Try to solve it again: ")
    root = find_root(p)
    print(f"root = {root}")


    print("try to find all roots at once: ")
    p = Polynomial([1, -9, 33, -63, 66, -36, 8])
    print(f"This is the polynomial: {p}")
    print(find_roots(p))

    print("try to find all roots at once: ")
    p = Polynomial([1, 1, 1])
    print(f"This is the polynomial: {p}")
    print(find_roots(p))

    print("try to find all roots at once: ")
    p = Polynomial([1, 0, -2])
    print(f"This is the polynomial: {p}")
    print(find_roots(p))