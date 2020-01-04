"""
    Generating Row of Pascal Triangle.

    for project euler 148, we need lucas theorem.

    This can also be used to test how good the polynomial class is at solving repeated roots.
"""


import math as m
__all__ = ["get_row"]

def get_row(r:int, j = None ):
    """
        Compute the jth element on the r th row.
    :param r:
        The row we are looking at.
    :return:
    """
    row = [None]*(r + 1)
    row[0] = row[-1] = 1
    for i in range(1, r//2 + 1):
        product = (row[i - 1]*(r - (i - 1)))//i
        row[i] = row[-i - 1] = product
    return row if j is None else row[j]

if __name__ == "__main__":
    print("Testing the method: ")
    res = get_row(10)
    print(res)
    res = get_row(9)
    print(res)
