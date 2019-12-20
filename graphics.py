"""
    This is the class that handles the graphics and it does the following:
    * It opens a window on the complex plane.
    * It shouldn't distort the ratio of the fractal for viewing.
    * It knows how many pixels are in the photos and automatically adjust the locations of the coordinates of the 4
    corners of the windows.
    * It can magnify into a certain points??? (How to do this....)
    * It can store the pixel value for each of the pixel in the image.
"""

from png import *
from typing import List
from typing import Tuple


class ComplexViewPort:

    def __init__(self, width: int, height: int, TopLeftCorner: complex, magnifier=1):
        """

        :param width:
            Thew width of the image in pixel, should be an integer.
        :param height:
            The length of the pixel in pixel, should be an integer.
        :param TopLeftCorner:
            The coordinate of the top left corner of the viewport.
        :param magnifier:
            1 means 100 pixel has length of 1 on the coordinate system.
            1.4 means 140 pixel has length of 1 on the coordinate system.
            you get the idea.
        """
        self.__ScaleMultiplier = 100
        assert width > 1 and height > 1, "View port width and height must be larger than 1. s"
        self.__Width = width; self.__height = height; self.__TopLeftCorner = TopLeftCorner; self.__Mag = magnifier
        self.__ImgData = [[(None, None, None) for y in range(self.__height)] for x in range(width)]
        return

    def __setitem__(self, PixelPosi: List[int], value: Tuple[int]):
        """

        :param PixelPosi:
            [x, y], [0, 0] is the top right corner of the image.
        :param value:
            (0~255, 0~255, 0~255) the value for the color of the pixel.
        :return:
            None.
        """
        x, y = PixelPosi
        if x < 0 or x > self.__width:
            return
        if y < 0 or y > self.__height:
            return
        self.__ImgData[x][y] = value

    def convert(self, ComplexNumber: complex):
        """
            Function convert the value of the complex number to a pixel position in the viewport.
        :param ComplexNumber:
            Any Complex Number
        :return:
            A pixel position with respect to the top left corner of the viewport. If it's outside of the image,
            then it will still return the value.
            The value will be in float.
        """
        r, i = ComplexNumber.real, ComplexNumber.imag
        # Relative position
        r, i = r - self.__TopLeftCorner.real, i - self.__TopLeftCorner.imag
        # Scale
        r, i = r*self.__ScaleMultiplier, i*self.__ScaleMultiplier
        return r, i




