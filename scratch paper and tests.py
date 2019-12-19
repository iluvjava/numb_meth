"""
    This class contain codes that assess the accuracy of the roots of the polynomial finding algorithm.

"""

from core_modules import *
from typing import Type
Mypolynomial = Type[Polynomial]


def main():
    test_root_finding_precision()


def test_root_finding_precision():
    p = Polynomial({20: 1, 0: -1})
    e = get_errors_for_poly(p)
    print(f"The maximum value deviation from the function is: {e}")
    p = Polynomial({50: 1, 0: -20})
    e = get_errors_for_poly(p)
    print(f"The maximum value deviation from the function is: {e}")
    p = Polynomial({300: 1, 0: -20})
    e = get_errors_for_poly(p)
    print(f"The maximum value deviation from the function is: {e}")
    pass


def get_errors_for_poly(p: Polynomial):
    """
    Given any polynomial, it will run the solve for the polynomial and then solve, then it will substitute the roots
    back to the polynomial and return a list of errors for the polynomials.
        * Assert the sum of the multiplicity of all roots match the maximum degree of the polynomials.
        * Substitute into the f(x) to get the maximum number deviated from zero.
    :param p:
        P is the polynomials
    :return:
        A list of error for each of the roots.
    """
    p = Polynomial({20: 1, 0: -1})
    roots = find_roots(p)
    assert sum(roots.values()) == p.deg(), "Sum of multiplicity doesn't match the maximum degree of the polynomials."
    errors = []
    for r in roots.keys():
        errors.append(abs(p.eval_at(r)))
    return max(errors)



if __name__=="__main__":
    main()




