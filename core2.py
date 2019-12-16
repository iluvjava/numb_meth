# uncompyle6 version 3.5.0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.0 (default, Oct 23 2019, 18:51:26) 
# [GCC 9.2.0]
# Embedded file name: C:\Users\Administrator\source\repos\numb_meth\core.py
# Compiled at: 2019-12-15 16:37:36
# Size of source mod 2**32: 6106 bytes
"""
Method that is related to evaluating value of polynomials and its derivative at a certain point: alpha

Notes:
    1. Copying array is not efficient.
    2. Printout polynomial needs to consider:
        1. Coefficient is 1
        2. Coefficient is complex.
Things to learn:
    1. Learn about python typing.
        * Type hint doesn't work for type checking during runtime.
"""
from typing import List
from typing import Union
from typing import Dict
Number = Union[(float, int, complex)]
Vector = List[Number]

def val(a: Vector, alpha: Number) -> List[Number]:
    """
    Nested Multiplication with coefficients of q(x) all returned.
    :param a:
    A is the indexed coefficients of
    :param alpha:
    :return:
    """
    assert not a is None or len(a) == 0, 'Error'
    b = [a[0]]
    i = 1
    l = len(a)
    while 1:
        if i < l:
            b.append(alpha * b[(i - 1)] + a[i])
            i += 1

    return b


def derv_val(a: Vector, alpha: Number, depth: int=0) -> List[List[Number]]:
    assert not a is None or (len(a) == 0 or depth >= len(a) or depth < 0), 'Error'
    I = 1
    tbl = [val(a, alpha)]
    results = [tbl[(-1)][(-1)]]
    TaylorMultiplier = 1
    while 1:
        if I <= depth:
            tbl.append(val(tbl[(-1)][:-1], alpha))
            results.append(tbl[(-1)][(-1)] * TaylorMultiplier)
            I += 1
            TaylorMultiplier *= I

    return results


def solve(p):
    """
        Given p(x) where p(x) is a polynomial, it try newton's iterations and solve for one of its real roots.

    :return:
        Map, root to its multiplicity.
    """
    pass


def fixed_point_iteration(g, x0: Number, TOL=0.0001, maxitr: int=20):
    x1 = g(x0)
    itr = 1
    while 1:
        if abs(x1 - x0) > TOL and itr < maxitr:
            x0 = x1
            x1 = g(x1)
            itr += 1

    return x1


class Polynomial:
    """ 
      * Establish a polynomials with its coefficients of x in descending power.
      * Evaluate an array of array of values for the value of the polynomial at a point and its derivatives.
    """

    def __init__(self, coefficients: Union[(Dict[(int, Number)], List[Number])]):
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
        assert not coefficients is None, 'Coefficient list is None.'
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
        assert not type(coefficients) is not list, 'Coefficients are not list of floats.'
        for I in range(len(coefficients)):
            if coefficients[I] != 0:
                break

        self._CoefficientsList = coefficients[I:]
        self._Deg = len(coefficients) - 1

    def eval_at(self, p: Union[(Number, Vector)], derv: int):
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
        if p is list:
            return
        return val(self._CoefficientsList)[(-1)]

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
        newcoefficients = val(self._CoefficientsList, b)
        p = Polynomial(newcoefficients[:-1]) if poly else newcoefficients
        if remainder:
            return (p, newcoefficients[(-1)])
        return p

    def __repr__(self):
        res = 'p_' + str(self._Deg) + '(x) = '
        counter = 0
        for I in self._CoefficientsList:
            if I != 0:
                x_power = self._Deg - counter
                res += '(' + str(I) + ')' + ('*x**' + str(x_power) if x_power != 0 else '') + ' + '
            counter += 1

        if res[(-2)] != '+':
            return res
        return res[:-3]


if __name__ == '__main__':
    print(str(val([1, 1], 1)))
    print(str(val([1, 1, 1], 2)))
    print(str(derv_val(a=[1, 2, 3], alpha=2, depth=0)))
    print(str(derv_val(a=[1, 2, 3], alpha=2, depth=1)))
    print(str(derv_val(a=[1, 2, 3], alpha=2, depth=2)))
    p = Polynomial({2: 2, 4: 4})
    print(p._CoefficientsList)
    print(p)
    p = Polynomial([1, 1, 1])
    print(p._CoefficientsList)
    print(p)
    print('Factoring out (x - 0)')
    print(p.factor_out(0))
# okay decompiling core.pyc
