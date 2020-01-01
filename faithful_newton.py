"""
    * Classic Newton Raphson iteration on polynomials. with examples.
    * It does this in a faithful manner

    credit:
        * Thank you, Sir Issac Newton, for torturing me through out my 4+ years of education, you are indeed a mastermind
        that is still controlling the world in your grave.
"""
from core_modules.core2 import *
from typing import Type
Mypolynomial = Type[Polynomial]
from core_modules.misc import *

def newton_iter(poly: Mypolynomial, x0: Number, relTOL=1e-4, maxitr=200):
    """
        it performs the newton Rapshson Iteration.
        This is not solving it in any way, it just carries out the iteration and store
        all the information with respect to the given initial conditions and parameters.

        It will solve the polynomials first, then uses the roots to conclude the convergence.
        It will also use the roots for fast and accurate evaluations of the function and the
        derivative of the function for all the iterating points.

        The iterating roots converge to a certain root given that it's in the range
        of 2 stander deviation from the solved root, this is the condition for absolute
        tolerance.

    :param poly:
        The polynomial object
    :param x0:
        The initial guess for roots
    :param relTOL:
        Tolerance for relative tolerance, measure by abs(x_{n} - x_{n+1})
    :param maxitr:
        maximum iterations to prevent infinite loop
    :return:
        an object, in the form of map, represented in following format:

    """

    return