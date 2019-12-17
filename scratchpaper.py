def main():
    p = Polynomial([1, 4, 6, 4, 1])
    solve(p, x0 = 0.5)
    pass

from core2 import *


def solve(p, x0:Number = None, TOL=1e-14, maxitr=1e2):
    """
        Given p(x) where p(x) is a polynomial, it try newton's iterations and solve for one of its real roots.

    :return:
        Map, root to its multiplicity.
    """
    x0 = random() if x0 is None else x0
    # fixed point iteration.

    def f(point):
        res = p.eval_at(point, derv=1)
        return point - res[0]/res[1]

    return fixed_point_iteration(f, x0, TOL, maxitr)


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
        dx = x0 - x1
        dy = x1 - g(x1)
        print(f"derivative at fixed point iteration: {dy/dx}, abs(x1 - x0) = {abs(x1 - x0)}, x"
              f"1 = {x1}")
        x0 = x1
        x1 = g(x1)
        itr += 1

    return x1







if __name__=="__main__":
    main()




