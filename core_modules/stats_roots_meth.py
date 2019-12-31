"""
    This file is concerned with storing the roots from the root finding algorithm, it should assist with the
    root precision for the polynomial evaluation.

    It's a naive solution for the problem

------------------------------------------------------------------------------------------------------------------------
What are we collecting?
------------------------------------------------------------------------------------------------------------------------
    1. We need all the roots obtained from multiple solves of the same polynomial.
    2. We will use then to compute the best estimated roots using basic statistics.

------------------------------------------------------------------------------------------------------------------------
What to keep in mind
------------------------------------------------------------------------------------------------------------------------
    1. There is going to he another script that refers to this script and the polynomial script that handles
    most of the thing about solving.

------------------------------------------------------------------------------------------------------------------------
What does it do?
------------------------------------------------------------------------------------------------------------------------
    * Construct an instance of RootsStore with an intial set of roots that are obtained upon first solving the
    polynomial.
    * Using the add_roots method to add set of roots obtained from subsequent solving.
    * Using the get_stats method to obtain statistics from the roots finding method, which will increase the precision
    of the roots, while also obtaining the range where the accurate roots are likely to be located at.
"""

from core_modules.core2 import *
from typing import Type, Dict
MyPolynomial = Type[Polynomial]

__all__ = ["ExtremeSolver"]


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
                [sum(|x1|), sum(|x2|), ...]
            ]
    """
    def __init__(self, First_Roots: Dict[Number, int]):
        self.__RootsContainer = []
        self.__AllRoots = []
        self.__RootsStats = [[], [], []]
        self.__SolveCount = 1
        for k in First_Roots.keys():
            self.__RootsContainer.append((k, First_Roots[k], [k]))
            self.__AllRoots.append([k])
            self.__RootsStats[0].append(k)
            self.__RootsStats[1].append(abs(k)**2)
            self.__RootsStats[2].append(abs(k))

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
                (root1_average, root1_sd)
            ]
        """
        stats = []
        for sum, absSquareSum, absSum, in zip(self.__RootsStats[0], self.__RootsStats[1], self.__RootsStats[2]):
            E_x = sum/self.__SolveCount
            E_abs_x2 = absSquareSum/self.__SolveCount
            E_abs_x = absSum/self.__SolveCount
            stats.append((E_x, E_abs_x2 - E_abs_x**2))
        return stats

    def get_results(self):
        """
            The result is the aggregated roots from running the roots finding repeatedly.
        :return:
            An list of array, it will have the following format:
        """

        return self.__AllRoots



class ExtremeSolver:
    """
        This class will take the solving scheme to absolute extreme and at the same time, having a more stable, simple
        API methods that easy to use and understand.

        The extreme solve will do the following:
            1. Produce the most accurate roots from multiple solving.
            2. Produce an upper bound and a lower bound for the roots.
    """
    def __init__(self, p: MyPolynomial, Repetition: int):
        """
            initiate the extreme solver with an instance of the polynomial.
        :param p:
            An instance of the polynomial class.
        :param Repetition:
            How many time you want to repeatedly solve the polynomial?
        """
        self.__P = p
        self.__Repetition = Repetition
        pass



if __name__ == "__main__":
    print("Ok we are going to run some tests here. ")
    p = Polynomial({100:1, 0:1})
    roots = p.get_roots()
    rs = RootsStore(roots)
    for I in range(100):
        rs.add_roots(p.get_roots())

    print(rs.get_results())
    print(rs.get_roots_info())
    print(rs.get_stat())