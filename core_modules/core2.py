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


from typing import Type, Dict
from random import random
from math import isnan
from typing import List, Union, Dict
import core_modules.misc as misc

Number = Union[float, int, complex]
Vector = List[Number]
__all__ = ["Polynomial", "Number", "Vector", "find_roots", "ExtremeSolver"]



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

            [!IMPORTANT] a_0 should not be zero! leading zeros will be trimmed
            :param coefficients:
                * a map, maps the power of x to its coefficients
                * a array, [a_0, a_1, a_2..., a_n]
            :except
                * A lot of exceptions
        """
        assert coefficients is not None, 'Coefficient list is None.'
        self.__Roots = None
        self.__Extreme_Solver = None
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

    def ponyval(self, x):
        """
            This is an alternative method for ill-conditioned polynomials.
            Perform a high precision evaluations of the polynomial using the roots of the polynomials.
        :param x
            The value for evaluations.
        :return:
            The value of the polynomial evaluated at that point.
        """
        if self.__Roots is None:
            self.__Roots = self.get_roots(Multiple_Solve=10)
        RunningProduct = self._CoefficientsList[0]
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
        return Polynomial(New_Coefficients) if poly else New_Coefficients

    def get_roots(self, active=True, Multiple_Solve: int = 1):
        """
            Get all the original roots for this polynomial using the modified Newton
            Raphson method.
        :param: active
            when active is set to true, it won't store the value from the previous solve
            and return it for the future.

            When active is set to false, it will return the roots from previous solve if
            it has been already calculated.

            default: True
        :param Multiple_Solve
            An integer that is greater or equal than 1.
            It will solve the roots of the polynomial multiple times and take the average of it,
            which will make it more accurate.
        :return:
            A map, with complex roots as key and the multiplicity as the value.
        """
        if self.__Roots is not None and not active:
            return self.__Roots
        if Multiple_Solve == 1:
            self.__Roots = find_roots(self)
            return self.__Roots
        if abs(Multiple_Solve) > 1:
            self.__Extreme_Solver = ExtremeSolver(self) if self.__Extreme_Solver is None else self.__Extreme_Solver
            self.__Extreme_Solver.solve_it(repetitions=abs(Multiple_Solve))
            # Extrac the result out and represent it in the classical way:
            the_Roots = dict()
            for root_Avg, sd, m in self.__Extreme_Solver.get_roots_data():
                the_Roots[root_Avg] = m
            self.__Roots = the_Roots
        return self.__Roots

    def normalized(self):
        """
        This method is created for the concern of numerical precision lots when the leading coefficients of the
        polynomial is extremely large.

        This will convert the polynomial with a leading coefficients of 1 where the resulting "normalized"
        polynomial will have the same roots compare to the previous one.
        :return:
            An instance of the normalized polynomial.
        """
        n = self._CoefficientsList[0]
        return Polynomial([x/n for x in self._CoefficientsList])


MyPolynomial = Type[Polynomial]


class RootsStore:
    """
        This class will be a naive way of storing the roots obtained from the stochastic process.

        Format of storing the roots in
            These info is obtained upon first solve and it will be used to organize roots upon subsequent solving.
        __RootsContainer:
            [(complex1, multiplicity, [complex2, complex3...]).....]

        Formats of storing the results:
            ???! These results might not be necessary at all.
        __AllRoots:
            [[root1, root1, root1...], [root2, root2, root2...]... ]

        Formats of storing the relevant info for stats
            Important intermediate results for computing the complex variance of the complex random variable.
        __RootsStats:
            [   [sum(x1), sum(x2), ...],
                [sum(|x1|^2), sum(|x2|^2), ...],
                [sum(|x1|), sum(|x2|), ...],
                [x1_multiplicity, x2_multiplicity, ....]
            ]
    """
    def __init__(self, First_Roots: Dict[Number, int]):
        self.__RootsContainer = []
        self.__AllRoots = []
        self.__RootsStats = [[], [], [], []]
        for k in First_Roots.keys():
            self.__RootsContainer.append((k, First_Roots[k], [k]))
            self.__AllRoots.append([k])
            self.__RootsStats[0].append(k)
            self.__RootsStats[1].append(abs(k)**2)
            self.__RootsStats[2].append(abs(k))
            self.__RootsStats[3].append(First_Roots[k])
        #  This could be unnecessary because it's given as the len of the inner array in __AllRoots.
        self.__SolveCount = 1

    def __get_index(self, Root: complex, Multiplicity: int):
        """
            Function attempts to add the new found root to the closest roots it can find from the first established
            set of roots.
        :param Root:
            A root that is found from future iterations.
        :param Multiplicity:
            The multiplicity of the root
        :return:
            The index of the root being inserted into the list of roots.
        """
        I = 0
        index = 0
        dis = abs(Root - self.__RootsContainer[0][0])
        for r, mul, arr in self.__RootsContainer:
            new_Distance = abs(Root - r)
            if new_Distance < dis and Multiplicity == mul:
                dis = new_Distance
                index = I
            I += 1
        return index

    def add_roots(self, Roots: Dict[Number, int]):
        """
            The method is going to test thing through first, so if there is something wrong with the roots,
            the stats won't be polluted.
        :param Roots:
            A set of roots returned by the get_roots method in the polynomial
        :return:
            None.
        """
        Indices = set()  # A set of unique index that the root upon subsequent solve should be inserted.
        Index_List = []  # A list of index where each root in the corresponding position in "Roots" should be added to
        Roots_List = []  # The list of roots extracted from iterating through "Roots".
        for k in Roots.keys():
            I = self.__get_index(k, Roots[k])
            if I in Indices:
                assert True, "2 or mores roots merge to the same root upon subsequent solving."
            Indices.add(I)
            Index_List.append(I)
            Roots_List.append(k)

        ## No errors, let's add the information in.

        for I, The_Root in zip(Index_List, Roots_List):
            self.__RootsContainer[I][2].append(The_Root)
            self.__AllRoots[I].append(The_Root)
            self.__RootsStats[0][I] += The_Root
            self.__RootsStats[1][I] += abs(The_Root)**2
            self.__RootsStats[2][I] += abs(The_Root)
        self.__SolveCount += 1
        return

    def get_roots_info(self):
        return self.__RootsContainer

    def get_stat(self):
        """
            Produce statistics about each of the roots from the intermediate data maintained.
            the formula for computing the variance of complex random variable is:
            E[|X|^2] - E[|X|]^2
        :return:
            a list of info about each of the found root, it's presented in the following format:
            [
                (root1_average, root1_sd),
                (root2_average, root2_sd),
                ...
                (root_n_average, root_n_sd)
            ]
        """
        stats = []
        counts = len(self.__AllRoots[0])
        for sum, absSquareSum, absSum, mul in\
                zip(self.__RootsStats[0], self.__RootsStats[1], self.__RootsStats[2], self.__RootsStats[3]):
            E_x = sum/counts
            E_abs_x2 = absSquareSum/counts
            E_abs_x = absSum/counts
            stats.append((E_x, E_abs_x2 - E_abs_x**2, mul))
        return stats

    def get_results(self):
        """
            The result is the aggregated roots from running the roots finding repeatedly.
        :return:
            An list of array, it will have the following format:
        """

        return self.__AllRoots

    def identify_root(self, root: Number):
        """
            Identify if the number you passed can be considered as a root of a polynomial.
        :param root:
            The root you want to identify
        :return:
            an index, positive and larger than 0, it's an representative assigned to each of the unique roots.
            a number representing the total number of unique roots of this polynomial.
            -1 is returned if it's not close enough to any of the roots of this polynomial.

            Stored in the following format:
            (int_representative, multiplicity)
        """
        assert False, "Method is not implemented yet."
        pass


class ExtremeSolver:
    """
        This class will take the solving scheme to absolute extreme and at the same time, having a more stable, simple
        API methods that easy to use and understand.

        The extreme solve will do the following:
            1. Produce the most accurate roots from multiple solving.
            2. Produce an upper bound and a lower bound for the roots.
    """
    def __init__(self, p: MyPolynomial):
        """
            initiate the extreme solver with an instance of the polynomial.
        :param p:
            An instance of the polynomial class.
        """
        self.__P = p
        self.__Cached = RootsStore(p.get_roots())
        pass

    def solve_it(self, repetitions: int = 10):
        """
        Method will attempt to solve the polynomial repeatedly and return a sets of roots and
        their respective standard deviation in complex plane.

        The stats will be cached for multiple solving as long as it's the same instance of the extreme_solve.

        :return:
            The roots averaged and the standard deviations of each of the root.
        """
        for I in range(repetitions):
            self.__Cached.add_roots(self.__P.get_roots())
        return self.__Cached.get_stat()

    def get_extreme_roots(self):
        """
            The a list extreme roots.
            Roots with multiplicity higher than 1 will get repeated in the array.
        :return:
            A set of very roots averaged out after the multiple solve.
        """
        res = []
        for r, sd, m in self.__Cached.get_stat():
            res.append(r)
        return res

    def get_sd(self):
        res = []
        for r, sd, m in self.__Cached.get_stat():
            res.append(sd)
        return res

    def get_roots_data(self):
        """

        :return:
            All of the data relevant to the root in a an array of tuple containing 4 element, in the following
            format:
                (root_avg, root_sd, root_multiplicity)
        """

        return self.__Cached.get_stat()


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
    l = len(a)
    b = [None]*l
    b[0] = a[0]
    i = 1
    while i < l:
        b[i] = (alpha * b[i - 1] + a[i])
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


def find_root(p: MyPolynomial, x0:Number=None, TOL = 1e-14):
    """
        Attempts to solve the polynomial at that point.
    :param p:
        The polynomial.
    :return:
        dict mappint the roots to it'ss multiplicity.
    """
    left, right = -1, 1
    x0 = complex((right - left)*random() - right, (right - left)*random() - right) if x0 is None else x0
    maxitr = 1e+4
    k = 0
    # The kth derivative
    retries = 0
    while k + 1 <= p.deg():

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

        # Blocks invalid\bad solution and try again with a new guess, x0
        if isnan(x1.real) or isnan(x1.imag) or abs(p.eval_at(x1)) > 1e-4:
            left *= 1.1
            right *= 1.1
            assert right < 2**900 and retries < 100, \
                f"Retries too many times something is wrong:" \
                f" \n {p} \n x1 ={x1} \n itr={itr} \n p(x1) = {p.eval_at(x1)} \n k = {k}"
            x0 = complex((right - left)*random() - right, (right - left)*random() - right)
            retries += 1
            continue

        def is_repeating_roots(p, k, x1):
            if k + 1 == p.deg():
                return False
            fx_point_derv = (g(x1 + 1e-4) - g(x1 - 1e-4))/1e-4
            return abs(fx_point_derv) > 1e-1

        if not is_repeating_roots(p, k, x1):
            return x1, k + 1
        k += 1
        continue

    return None # Not converging.


def find_roots(p: MyPolynomial, results: Dict[Number, int] = None, precision:str = None, last_Root = None):
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
    root, multiplicity = find_root(p, last_Root)
    root_roundup = roundup(root, precision)
    results[root_roundup] = multiplicity
    p = p.factor_out(root, multiplicity=multiplicity, poly=True)
    p = p.normalized()  # Normalized the polynomial after factoring out the previously found root.
    return find_roots(p, results=results, precision=precision, last_Root = roundup(root_roundup, precision="low"))


if __name__ == '__main__':
    pass












