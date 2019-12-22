"""
    This file is concerned with storing the roots from the root finding algorithm, it should assist with the
    root precision for the polynomial evaluation.
"""

from core_modules.core2 import *
from typing import Type, Dict
MyPolynomial = Type[Polynomial]


class RootsStore:
    """
        This class will be a naive way of storing the roots obtained from the stochastic process.

        Format of storing the roots.
        [(complex1, multiplicity, [complex2, complex3...]).....]
    """

    def __init__(self, First_Roots: Dict[Number, int]):
        self.__RootsContainer = []
        for k in First_Roots.keys():
            self.__RootsContainer.append((k, First_Roots[k], []))


    def __add_new_root(self, Root: complex, Multiplicity: int):
        """
            Function attempts to add the new found root to the closest roots it can find from the first established
            set of roots.

        :param Root:
            A root that is found from future iterations.
        :param Multiplicity:
            The multiplicity of the root
        :return:
            None.
        """
        I = 0
        index = 0
        dis = abs(Root - self.__RootsContainer[0][0])
        for r, mul, arr in self.__RootsContainer:
            new_Distance = abs(Root - r)
            if new_Distance < dis and Multiplicity == self.__RootsContainer[I][1]:
                dis = new_Distance
                index = I
            I += 1
        self.__RootsContainer[index][2].append(Root)
        return

    def add_roots(self, Roots: Dict[Number, int]):
        for k in Roots.keys():
            self.__add_new_root(k, Roots[k])
        pass

    def get_stat(self):
        return self.__RootsContainer

if __name__ == "__main__":
    print("Ok we are going to run some tests here. ")
    p = Polynomial([1, 1, 1, 1])
    roots = p.get_roots()
    rs = RootsStore(roots)

    rs.add_roots(p.get_roots())
    print(rs.get_stat())
