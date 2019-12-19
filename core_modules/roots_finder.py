"""
    Given a polynomial, we find its roots and the corresponding geometric multiplicity, high precision

------------------------------------------------------------------------------------------------------------------------
Algorithm:
------------------------------------------------------------------------------------------------------------------------
Basic idea:
    * Use Newton's method too look for the roots of the polynomials.
    * Use derivative to determine the repeated roots and them optimize it for accuracy.

------------------------------------------------------------------------------------------------------------------------
Problems:
------------------------------------------------------------------------------------------------------------------------
    * false evaluation of the derivative of the fixed point iterative function
      for polynomials with extremely large degree.
      * could be solved by taking better guess for system that are very stiff around certain intervals, reasonable
        polynomial can't be stiff over all the real numbers.

"""

__all__ = ["find_roots"]

from core_modules.core2 import *
from typing import Type, Dict
from random import random
MyPolynomial = Type[Polynomial]


def find_root(p: MyPolynomial, x0: Number=None):
    """
        Attempts to solve the polynomial at that point.
    :param p:
        The polynomial.
    :return:
        dict mappint the roots to it'ss multiplicity.
    """
    left, right = -1, 1
    x0 = complex((right - left)*random() - right, (right - left)*random() - right) if x0 is None else x0
    TOL = 1e-14
    maxitr = 1e4
    k = 0
    # The kth derivative

    while k + 1 <= p._Deg:
        # define fixed point function
        def g(point):
            res = p.eval_all(point, derv=k + 1)
            return point - (res[k] / res[k + 1])

        # Start fixed point iteration.
        itr = 0
        x1 = g(x0)
        while abs(x0 - x1) > TOL and itr < maxitr:
            if abs(p.eval_at(x0, k + 1)) < 1e-3: # bad initial guess
                left *= 2; right *= 2
                x0 = complex((right - left)*random() - right, (right - left)*random() - right)
                x1 = g(x0)
                continue
            x0 = x1
            x1 = g(x1)
            itr += 1

        # Blocks invalid solution:
        assert abs(p.eval_at(x1)) < 1e-4, f"Grave Error omg. x1 = {x1}, maxitr reached? :{itr == maxitr}"

        # Checking the fixed point function result for repeated roots.
        dgdx = (g(x1 + 1e-8) - g(x1))/1e-8
        if abs(dgdx) < 1e-2:
            return x1, k + 1
        k += 1
        continue
    return None # Not converging.


def find_roots(p: MyPolynomial, results:Dict[Number, int] = None, precision:str = None):
    """
        Function find all the roots of the polynomials.
    :param p:
        The polynomials we want to solve.
    :param results:
        All the roots and it's corresponding multiplicity returned in a map.
    :param precision:
        The precision your want for your roots.
        original is just None, "high" precision: 10e-10, "medium" precision 10e-6, "low" precision: 10-e-4
    :return:
        a map in the format of {root1: multiplicity, root2: multiplicity.......}
    """

    if p.deg() > 20 and results is None:
        print("\033[93m" + "[Warning:] Polynomial has a degree higher than 20, root finding algorithm might fail "
              "due to stiffness at the point near first guess or other reasons." + "\033[0m")

    def roundup(root: Number, precision: str):
        """
            Round up the error according to the precision arguments.
        :param root:
            One of the roots
        :return:
            A rounded up version.
        """
        options = {"high": 10, "median": 6, "low": 4}
        if precision is None:
            return root
        precision = precision.strip().lower()
        rounded = complex(round(root.real, options[precision]), round(root.imag, options[precision]))
        if rounded.real == 0 and rounded.imag == 0:
            return 0
        if rounded.real == 0:
            return rounded.imag
        if rounded.imag == 0:
            return rounded.real
        return rounded

    results = results if results is not None else {}
    if p.deg() == 0:
        return results
    root, multiplicity = find_root(p)
    results[roundup(root, precision)] = multiplicity
    p = p.factor_out(root, multiplicity=multiplicity, poly=True)
    return find_roots(p, results, precision)



if __name__ == "__main__":

    p = Polynomial({50: 1, 0: -1})
    print(f"Try to find the roots for: {p}")
    print(find_roots(p, precision="high"))

    p = Polynomial({100: 1, 0: -1})
    print(f"Try to find the roots for: {p}")
    print(find_roots(p, precision="high"))
