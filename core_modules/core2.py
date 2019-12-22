"""
Method that is related to evaluating value of polynomials and its derivative at a certain point: alpha

Notes:
    1. Copying array is not efficient.
    2. Printout polynomial needs to consider:
        1. Coefficient is 1
        2. Coefficient is complex.
    3. Repeated Roots have bad convergence and accuracy.
        1. solution:
            1. Detect the repeating roots from slow convergence rate in a strict way
            2. Use it's derivative to look for the root.
Things to learn:
    1. Learn about python typing.
        * Type hint doesn't work for type checking during runtime.
"""

"""
    Given a polynomial, we find its roots and the corresponding geometric multiplicity, high precision

------------------------------------------------------------------------------------------------------------------------
Algorithm:
------------------------------------------------------------------------------------------------------------------------
Basic idea:
    * Use Newton's method too look for the roots of the polynomials.
    * Use derivative to determine the repeated roots and them optimize it for accuracy.


"""

__all__ = ["Polynomial", "Number", "Vector", "find_roots"]

from typing import List, Union, Dict
Number = Union[float, int, complex]
Vector = List[Number]

from typing import Type, Dict
from random import random
from math import isnan


class Polynomial:
    """
      * Establish a polynomials with its coefficients of x in descending power.
      * Evaluate an array of array of values for the value of the polynomial at a point and its derivatives.
    """

    def __init__(self, coefficients: Union[Dict[int, Number], List[Number]]):
        """
            Constructor.
            self._CoefficientsList:
                [a_0, a_1, a_2... a_n]

            self._Deg:
                The maximum power of x in the polynomial.

            a_0 should not be zero! leading zeros will be trimmed.
            :param coefficients:
                * a map, maps the power of x to its coefficients
                * a array, [a_0, a_1, a_2..., a_n]
            :except
                * A lot of exceptions
        """
        assert coefficients is not None, 'Coefficient list is None.'
        self.__Roots = None
        self._CoefficientsList = None
        self._Deg = None

        if type(coefficients) is dict:
            assert not len(coefficients.keys()) == 0, 'Coefficient list is empty.'
            lst = list(coefficients.keys())
            pow_max = max(lst)
            a = [0] * (pow_max + 1)
            for I in range(pow_max + 1):
                if I in coefficients.keys():
                    a[pow_max - I] = coefficients[I]

            self._CoefficientsList = a
            self._Deg = pow_max
            return # !!!
        assert type(coefficients) is list, 'Coefficients are not list of floats.'
        for I in range(len(coefficients)):
            if coefficients[I] != 0:
                break

        self._CoefficientsList = coefficients[I:]
        self._Deg = len(coefficients) - 1

    def eval_all(self, p: Union[Number, Vector], derv: int = 0):
        """
                returns the value evaluated at p, or a list of value.
            :param p: point or points that evaluate the function at.
            :param derv: The depth of derivative for this polynomials you also want while evaluating it at p.
            :return:
                if derv = 0, then it will return the value of polynomial evaluated at a point or a list of points.
                else
                    it will return a list of list where the first list is the 0th derivative, second list is the first.
                    etc
                it will always return a list of numbers.
        """
        assert not derv < 0 or derv > self._Deg, 'Derivative for Polynomial not Valid.'
        res = []
        if type(p) is list:
            for value in p:
                res.append(self.eval_at(value, derv))
            return res
        # p is not a list
        if derv == 0:
            return val(self._CoefficientsList, p)[-1]
        # p is a single value and derv is more than 0
        return derv_val(self._CoefficientsList, p, derv)

    def eval_at(self, p: Number, derv: int = 0):
        """
            Evaluate the polynomial or its derivative at that one point.
        :param p:
            The point you want to evaluate the polynomial.
        :param derv:
            The depth of derivative you want to evaluate the polynomial at.
        :return:
            p^{(k)}(p)
        """
        assert not(derv < 0 or derv > self._Deg), 'Derivative for Polynomial not Valid.'
        return derv_val(self._CoefficientsList, p, derv)[derv]

    def factor_out(self, b: Number, poly: bool = False, multiplicity: int=1):
        """
                return q(x) such that p(x) = q(x)(x - b) + R, where R is a constant.
            :param b:
            :param poly:
                Where you want to get an instance of Polynomial to be returned.
            :param remainder:
            :return:
                (q(x)|[a_0, a_1, ...], R) if both is required
                q(x) or coefficents of q(x) depends on poly.
                R: The remainder if required.
        """
        assert multiplicity <= self._Deg and multiplicity > 0,\
            "Cannot factor because multiplicity larger than max deg. "
        newCoefficients = self._CoefficientsList
        while multiplicity >= 1:
            newCoefficients = val(newCoefficients, b)[:-1]
            multiplicity -= 1

        p = Polynomial(newCoefficients) if poly else newCoefficients
        return p

    def __repr__(self):
        res = 'p_' + str(self._Deg) + '(x) = '
        counter = 0
        for I in self._CoefficientsList:
            if I != 0:
                x_power = self._Deg - counter
                res += '(' + str(I) + ')' + ('*x**' + str(x_power) if x_power != 0 else '') + ' + '
            counter += 1
        if res[-2] != '+':
            return res
        return res[:-3]

    def deg(self):
        """

        :return:
            The degree of the polynomial.
        """
        return self._Deg

    def eval_alt(self, x):
        """
            This is an alternative method for ill-conditioned polynomials.
            Perform a high precision evaluations of the polynomial using the roots of the polynomials.
        :param x
            The value for evaluations.
        :return:
            The value of the polynomial evaluated at that point.
        """
        if self.__Roots is None:
            self.__Roots = find_roots(self)
        RunningProduct = 1
        for r in self.__Roots.keys():
            RunningProduct *= (x - r)**self.__Roots[r]
        return RunningProduct

    def derv_analytical(self, poly=False):
        """
            This function produce the coefficients for the derivative polynomial.
        :param: poly
            Set it to True if you want the function to return an instance of polynomial, False if
            you only want an array of coefficients of the polynomial.
        :return:
            An array representing all coefficients of the returned polynomials, or
            an new instance of a polynomials.
        """
        New_Coefficients = []
        for I in range(len(self._CoefficientsList) - 1):
            New_Coefficients.append(self._CoefficientsList[I]*(self._Deg - I));
        return New_Coefficients

    def get_roots(self, active=True):
        """
            Get all the original roots for this polynomial using the modified Newton
            Raphson method.
        :param: active
            when active is set to true, it won't store the value from the previous solve
            and return it for the future.
            When active is set to false, it will return the roots from previous solve if
            it has been already calculated.
        :return:
            A map, with complex roots as key and the multiplicity as the value.
        """
        if self.__Roots is not None and not active:
            return self.__Roots
        self.__Roots = find_roots(self)
        return self.__Roots


MyPolynomial = Type[Polynomial]


def val(a: Vector, alpha: Number) -> List[Number]:
    """
        Nested Multiplication with coefficients of q(x) all returned.
    :param a:
        A is the indexed coefficients of
    :param alpha:
        The value you want to evaluate the function at.
    :return:
    """
    assert not(a is None or len(a) == 0), 'Error'
    b = [a[0]]
    i = 1
    l = len(a)
    while i < l:
        b.append(alpha * b[i - 1] + a[i])
        i += 1
    return b


def derv_val(a: Vector, alpha: Number, depth: int=0) -> List[List[Number]]:
    assert a is not None or (len(a) == 0 or depth >= len(a) or depth < 0), 'Error'
    I = 1
    tbl = [val(a, alpha)]
    results = [tbl[-1][-1]]
    TaylorMultiplier = 1
    while I <= depth:
        tbl.append(val(tbl[-1][:-1], alpha))
        results.append(tbl[-1][-1] * TaylorMultiplier)
        I += 1
        TaylorMultiplier *= I
    return results


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
    TOL = 1e-15
    maxitr = 1e4
    k = 0
    # The kth derivative

    while k + 1 <= p._Deg:
        # define fixed point function
        def g(point):
            res = p.eval_all(point, derv=k + 1)
            return point - (res[k] / res[k + 1])

        # Start fixed point iteration with good and stable initial guess x0 for the kth iteration
        x1 = g(x0)
        itr = 0
        while abs(x0 - x1) > TOL and itr < maxitr:
            x0 = x1
            x1 = g(x1)
            itr += 1

        # Blocks invalid solution and try again with a new guess, x0
        if isnan(x1.real) or isnan(x1.imag) or abs(p.eval_at(x1)) > 1e-4:
            left *= 2
            right *= 2
            x0 = complex((right - left)*random() - right, (right - left)*random() - right)
            continue

        # assert abs(p.eval_at(x1)) < 1e-4, f"Grave Error omg. x1 = {x1}, maxitr reached? :{itr == maxitr}"

        # Checking the fixed point function result for repeated roots.
        dgdx = (g(x1 + 1e-8) - g(x1))/1e-8
        if abs(dgdx) < 1e-2:
            return x1, k + 1 # Root attained.
        k += 1
        continue

    return None # Not converging.


def find_roots(p: MyPolynomial, results: Dict[Number, int] = None, precision:str = None):
    """
        Function find all the roots of the polynomials, runtime of the method is not bounded because of the
        stochastic process involved.
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
        print("\033[93m" + "[Warning]: Polynomial has a degree higher than 20, root finding algorithm might fail "
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



if __name__ == '__main__':
    p = Polynomial([1, 1, 1])
    print(p)
    res = p.eval_all(1, derv=2)
    print(res)

    res = p.eval_all([x/100 for x in range(100)])
    print(res)

    p = Polynomial([1]*100) # should be 1/(1-x) for x in (-1, 1)
    print(p.eval_all(-0.5))

    p = Polynomial([1/x for x in range(100, 0, -1)] + [0]) # should be ln(1-x) for x in (-1, 1)
    print(p.eval_all(-0.5, 3))

    p = Polynomial([1, 2, 1])
    print("A thing about truncation error: ")
    print(p.eval_all(-1 - 1e-13, derv=2))

    print("Slow convergence and bad accuracy for repeated roots. ")
    print("Testing Eval_at functionality: ")

    p = Polynomial([1, 1, 1])
    print(p)

    print(f"Evaluating p''(1): {p.eval_at(1, derv=2)}")
    print(f"Evaluating p'(1): {p.eval_at(1, derv=1)}")
    print(f"Evaluating p(1): {p.eval_at(1)}")

    p = Polynomial({50: 1, 0: -1})
    print(f"Try to find the roots for: {p}")
    print(find_roots(p, precision="high"))

    p = Polynomial({100: 1, 0: -1})
    print(f"Try to find the roots for: {p}")
    print(find_roots(p, precision="high"))

    p = Polynomial([1, 3, 3, 1])
    print(f"Try to rind the roots for {p}")
    print(find_roots(p))
