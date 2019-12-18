"""
    * Classic Newton Raphson iteration on polynomials. with examples.
    * It does this in a faithful manner

    credit:
        * Thank you, Sir Issac Newton, for torturing me through out my 4+ years of education, you are indeed a mastermind
        that is still controlling the world in your grave.
"""
from core2 import *
from typing import Type
Mypolynomial = Type[Polynomial]


def newton_iter(poly: Mypolynomial, x0: Number, TOL, maxitr):
    """
        it performs the newton raphson iteration.
    :param poly:
        The polynomial object
    :param x0:
        The initial guess for roots
    :param TOL:
        Tolerance for exit conditions
    :param maxitr:
        maximum iterations to prevent infinite loop
    :return:
        The endpoint it converges to.
    """

    pass

