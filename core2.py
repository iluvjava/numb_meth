"""
Method that is related to evaluating value of polynomials and its derivative at a certain point: alpha

Notes:
    1. Copying array is not efficient.
    2. Printout polynomial needs to consider:
        1. Coefficient is 1
        2. Coefficient is complex.
    3. Repeated Roots have bad convergence, consider truncation error for derivatives evaluation.
Things to learn:
    1. Learn about python typing.
        * Type hint doesn't work for type checking during runtime.
"""
from typing import List, Union, Dict
Number = Union[float, int, complex]
Vector = List[Number]

from random import random

def val(a: Vector, alpha: Number) -> List[Number]:
    """
    Nested Multiplication with coefficients of q(x) all returned.
    :param a:
    A is the indexed coefficients of
    :param alpha:
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


def solve(p, x0:Number = None, TOL=1e-14, maxitr=1e2):
    """
        Given p(x) where p(x) is a polynomial, it try newton's iterations and solve for one of its real roots.

    :return:
        Map, root to its multiplicity.
    """
    x0 = random() if x0 is None else x0
    def f(point):
        res = p.eval_at(point, derv=1)
        return point - res[0]/res[1]
    return fixed_point_iteration(f, x0, TOL=TOL, maxitr=maxitr)


def fixed_point_iteration(g, x0: Number, TOL=1e-14, maxitr: int=20):
    """
    :param g:
        The fixed point iteration function
    :param x0:
        The initial guess.
    :param TOL:
        The tolerance
    :param maxitr:
        The maximum number of iteration
    :return:
        None if not converging.
    """
    x1 = g(x0)
    itr = 1
    while abs(x1 - x0) > TOL and itr < maxitr:
        x0 = x1
        x1 = g(x1)
        itr += 1
    return x1


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
            return
        assert type(coefficients) is list, 'Coefficients are not list of floats.'
        for I in range(len(coefficients)):
            if coefficients[I] != 0:
                break

        self._CoefficientsList = coefficients[I:]
        self._Deg = len(coefficients) - 1

    def eval_at(self, p: Union[Number, Vector], derv: int = 0):
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

    def factor_out(self, b: Number, poly: bool, remainder: bool):
        """
            return q(x) such that p(x) = q(x)(x - b) + R, where R is a constant.
        :param b:
        :param poly:
        :param remainder:
        :return:
            (q(x)|[a_0, a_1, ...], R) if both is required
            q(x) or coefficents of q(x) depends on poly.
            R: The remainder if required.
        """
        newCoefficients = val(self._CoefficientsList, b)
        p = Polynomial(newCoefficients[:-1]) if poly else newCoefficients
        if remainder:
            return p, newCoefficients[-1]
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


if __name__ == '__main__':
    p = Polynomial([1, 1, 1])
    print(p)
    res = p.eval_at(1, derv=2)
    print(res)

    res = p.eval_at([x/100 for x in range(100)])
    print(res)

    p = Polynomial([1]*100) # should be 1/(1-x) for x in (-1, 1)
    print(p.eval_at(-0.5))

    p = Polynomial([1/x for x in range(100, 0, -1)] + [0]) # should be ln(1-x) for x in (-1, 1)
    print(p.eval_at(-0.5, 3))

    p = Polynomial([1, 0, -2])
    print(solve(p))

    p = Polynomial([1, 3, 3, 1])
    print(solve(p, TOL=0, maxitr=1e10))


