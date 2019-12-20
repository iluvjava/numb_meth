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
        assert width > 1 and height > 1, "View port width and height must be larger than 1. s"
        self.__Width = width; self.__height = height; self.__TopLeftCorner = TopLeftCorner; self.__Mag = magnifier
        return


