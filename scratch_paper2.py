"""
    Just scratch paper.

"""

from numpy import *
import math as m
from typing import List, Type
Number = Type[int, float, complex]


def f(x):
    def inner_f(xx):
        return m.cos(2*xx) + m.sin(xx)
    if type(x) is not ndarray:
        return inner_f(x)
    res = []
    for n in x:
        res.append(inner_f(n))
    return res

def nth_roots_unity(N:int):
    """
        Function returns an numpy ndarray containing the Nth roots unity.
    :param N:
        The number of unity
    :return:
        a python array, represented in the following order:
        [1,
        exp(i((2*pi)/N)*1),
        exp(i((2*pi)/N)*2),
        exp(i((2*pi)/N)*3),
        ...
        exp(i((2*pi)/N)*(N - 1))
        ]
    """
    assert N >=1
    res = []
    for I in range(N):
        res.append(m.e**(complex(0, (2*m.pi)/N)*I))
    return res


def pony_multiply(P1:List[Number], N1:int, P2:List[Number], N2:int):
    """
        Multiply together 2 polynomial, using their coefficients.
        Assume Polynomial is represented as the following:
        p(x) := a_0*x^{N1} + a_1*x^{N1 - 1} + a_2*x^{N1 - 2} + ... + a_{N1 - 1}*x + a__{N1}
    :param P1:
        An array, the coefficients of the polynomial, the order of the coefficients should be:
        [a_0, a_1, ... a_{N1 - 1}, a_{N1}]
    :param N1:
        The maximum power of the polynomial, the degree.
    :param P2:
        The second polynomial, represented in the same way as the first one.
    :param N2:
        The leading power of the second polynomial .
    :return:
        The coefficients of the polynomial after the multiplications.
        [
            [real(c_0), real(c_1), real(c_2)... real(c_{N1 + N2})],
            [imag(c_0), imag(c_1), imag(c_2)... imag(c_{N1 + N2})
        ]
    """
    assert N1 >= 0 and N2 >= 0, "The degree of the polynomial must be a non-negative integer. "
    P = lambda x: polyval(P1, x)
    Q = lambda x: polyval(P2, x)
    PQ = lambda x: P(x)*Q(x)
    aggregate_Deg = N1 + N2
    qry_Points = nth_roots_unity(aggregate_Deg + 1)
    output_Values = []
    for I in qry_Points:
        output_Values.append(PQ(I))
    return fft.ifft(output_Values)


def main():

    # preparing the linspace
    xs = linspace(0, m.pi*2, 2**8)
    y = f(xs)
    res = fft.fft(y)
    print(f"This is the coefficients for cos:\n {res.real}")
    print(f"This is the coefficients for sin:\n {res.real}")
    recovered_y = fft.ifft(res)
    inf_Error_Norm = linalg.norm(recovered_y - y, inf)
    print("Here is the error norm after the fourier: ")
    print(inf_Error_Norm)

    print("This is the Nth roots of unity with N = 4:")
    res = nth_roots_unity(4)
    print(res)

    print("Trying to test the multiplying capability of the the function: ")




if __name__ == "__main__":
    main()