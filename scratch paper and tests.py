"""
    This class contain codes that assess the accuracy of the roots of the polynomial finding algorithm.

"""

from core_modules import *
from typing import Type
import math as m
from binomial_coefficients import *
Mypolynomial = Type[Polynomial]


def main():
    # test_root_finding_precision()
    # error_demo()
    # test_analytical_deriv(Polynomial([1, 1, 1, 1]))
    extremesolve_demo()


def test_root_finding_precision():
    p = Polynomial({20: 1, 0: -1})
    e = get_errors_for_poly(p)
    print(f"The maximum value deviation from the function is: {e}")
    p = Polynomial({50: 1, 0: -20})
    e = get_errors_for_poly(p)
    print(f"The maximum value deviation from the function is: {e}")
    p = Polynomial({100: 1, 0: -20})
    e = get_errors_for_poly(p)
    print(f"The maximum value deviation from the function is: {e}")
    p = Polynomial({200: 1, 0: -20})
    e = get_errors_for_poly(p)
    print(f"The maximum value deviation from the function is: {e}")
    pass


def get_errors_for_poly(p: Mypolynomial):
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
    roots = find_roots(p)
    assert sum(roots.values()) == p.deg(), "Sum of multiplicity doesn't match the maximum degree of the polynomials."
    errors = []
    for r in roots.keys():
        errors.append(abs(p.eval_at(r)))
    return max(errors)


def error_demo():
    """
        Method demonstrates the numerical accuracy problem for polynomials having a very high degree as its
        leading coefficients.
        * Test set up:
            p(x) = x^3 + 3x^2 + 3x + 1
            then using nested multiplication, eval at x = -1 + 1e-6
            observe that: p(1e-6 - 1) = 0.0
    :return:
        Your mom, the fuck you actually read my comments?
    """
    p = Polynomial([1, 3, 3, 1])
    print("Eval p(x) = x^3 + 3x^2 + 3x + 1 using nested multiplications. ")
    x = 1e-6 - 1
    print(f"at x = {x} then p(x) = {p.eval_at(x)}")
    print("However if given the roots of the polynomials, we can use the product and root's multiplicity for fast"
          "evaluation.")
    print(f"Roots: {p.get_roots()}")
    print("Using the high precision product evaluation, we have: ")
    v = p.ponyval(x)
    print(f"at x = {x}; p(x) = {v}")
    assert abs(1e-18 - v) < 1e-20, "Error too big, please look into it."

    print("We are trying to use multiple solves and the extreme solver to further increase the precison: ")
    print(f"Roots multiple solves: {p.get_roots(Multiple_Solve=100)}")
    v = p.ponyval(x)
    print(f"at x = {x}; p(x) = {v}")
    assert abs(1e-18 - v) < 1e-20, "Error too big, please look into it."
    print("Therefore, the ponyval function has proven it's numerical superiority.")


def test_analytical_deriv(p):
    """
        Function will test the analytical approach to taking the derivative of the polynomial.
    :return:
    """
    print(p.derv_analytical())
    pass


def extremesolve_test(degree: int = 20, repeatition: int = 100):
    """
        Test the accuracy of the method, both using the output value of the roots
        and compare the roots to the the correct solution of the roots.
    :return:
        None
    """
    p = Polynomial({degree: 1, 0: -1})
    es = ExtremeSolver(p)

    # Some helpful functions for our tasks.

    def correct_root(i):
        p1 = m.pi
        return complex(m.cos(((2*p1)/degree)*i), m.sin(((2*p1)/degree)*i))

    def find_distances(Correct_Soln, Extreme_Roots):
        distance = []
        for r in Extreme_Roots:
            distance.append(min([abs(x - r) for x in Correct_Soln]))
        return distance

    correct_Roots = [correct_root(i) for i in range(degree)]

    # Solving using extreme solver, repeating 100 times.
    es.solve_it(repeatition)
    distances = find_distances(correct_Roots, es.get_extreme_roots())
    return distances


def extremesolve_demo():

    print("Running codes that can demonstrate and measure the errors using the "
          "roots of unity.")
    upper_Limit, lower_Limit =30, 5 # inclusive
    print(f"bounded above by a degree of: {upper_Limit}, bounded below by a degree of {lower_Limit}")

    for degree in range(lower_Limit, upper_Limit + 1):
        errors = extremesolve_test(degree, repeatition=10)
        max_Error = max(errors)
        average_Error = sum(errors)/len(errors)
        print(f"degree: {degree}, max_error = {max_Error}, average_error = {average_Error}")

    #  Testing Extreme solve with repeated roots:
    print("We are going to use the classic repeating roots to test for how well multiple solving scheme functions.")
    p = Polynomial([1, 4, 6, 4, 1])
    es = ExtremeSolver(p)
    es.solve_it(repetitions=100)
    print(f"This is the data for the roots: \n{es.get_roots_data()}")

    print("Ok let's try something hellish and see if it can still work with that: ")
    coefficients = get_row(10)
    print(f"This is a coefficients we have for the polynomial: {coefficients}")
    print("The solution for the polynomial should be x = -1")
    p = Polynomial(coefficients)
    the_Roots = p.get_roots()
    print(f"Here is the solution from {the_Roots}")

    print("Ok let's try to make it even worse and see if it can find the root with a multiplicity of 20: ")
    coefficients = get_row(20)
    print(f"This is the list of coefficients for the polynomial: {coefficients}")
    p = Polynomial(coefficients)
    for I in range(10):
        the_Roots = p.get_roots()
        print(f"Here is the result from the root search: {the_Roots}")
    return



if __name__=="__main__":
    main()




