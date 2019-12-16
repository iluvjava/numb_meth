
���]�  �            	   @   s+  d  Z  d d l m Z d d l m Z d d l m Z e e e e f Z e e Z	 e	 e e e d d d � �  Z
 d e	 e e e e e d d	 d
 � � Z d d �  Z d d e e d d d � � Z Gd d �  d � Z e d k r'e e e
 d d g d � � � e e e
 d d d g d � � � e e e d d d d g d d d d � � � e e e d d d d g d d d d � � � e e e d d d d g d d d d � � � e d d d d i � Z e e j � e e � e d d d g � Z e e j � e e � e d � e e j d � � d S)az  
Method that is related to evaluating value of polynomials and its derivative at a certain point: alpha

Notes:
    1. Copying array is not efficient.
    2. Printout polynomial needs to consider:
        1. Coefficient is 1
        2. Coefficient is complex.
Things to learn:
    1. Learn about python typing.
        * Type hint doesn't work for type checking during runtime.
�    )�List)�Union)�Dict)�a�alpha�returnc             C   s�   |  d k s t  |  � d k r* t d � � |  d g } d } t  |  � } x; | | k  r� | j | | | d |  | � | d 7} qL W| S)z�
    Nested Multiplication with coefficients of q(x) all returned.
    :param a:
    A is the indexed coefficients of
    :param alpha:
    :return:
    Nr   �Error�   )�len�	Exception�append)r   r   �b�i�l� r   �5C:\Users\Administrator\source\repos\numb_meth\core.py�val   s    !r   )r   r   �depthr   c             C   s�   |  d  k s< t  |  � d k s< | t  |  � k s< | d k  rH t d � � d } t |  | � g } | d d g } d } xa | | k r� | j t | d d  d � | � � | j | d d	 | � | d 7} | | 9} qz W| S)
Nr   r   r	   �����r   r   r   r   r   )r
   r   r   r   )r   r   r   �I�tbl�results�TaylorMultiplierr   r   r   �derv_val'   s    <$
r   c             C   s   d S)z�
        Given p(x) where p(x) is a polynomial, it try newton's iterations and solve for one of its real roots.

    :return:
        Map, root to its multiplicity.
    Nr   )�pr   r   r   �solve5   s    	r   g-C��6?�   )�x0�maxitrc             C   s[   |  | � } d } xB t  | | � | k rV | | k  rV | } |  | � } | d 7} q W| S)Nr	   )�abs)�gr   ZTOLr   �x1Zitrr   r   r   �fixed_point_iterationA   s    %r"   c               @   s�   e  Z d  Z d Z e e e e f e e f d d d � �  Z	 e e e
 f e d d d � �  Z e e e d d	 d
 � �  Z d d �  Z d S)�
Polynomialz�
    * Establish a polynomials with its coefficients of x in descending power.
    * Evaluate an array of array of values for the value of the polynomial at a point and its derivatives.
    )�coefficientsc             C   sH  | d k r t  d � � t | � t k r� t | j �  � d k rN t  d � � t | j �  � } t | � } d g | d } x< t | d � D]* } | | j �  k r� | | | | | <q� W| |  _ | |  _	 d St | � t k	 r� t  d � � x+ t t | � � D] } | | d k rPqW| | d � |  _ t | � d |  _	 d S)a�  
        Constructor.
        self._CoefficientsList:
            [a_0, a_1, a_2... a_n]

        self._Deg:
            The maximum power of x in the polynomial.

        a_0 should not be zero! leading zeros will be trimmed.
        :param coefficients:
            * a map, maps the power of x to its coefficients
            * a array, [a_0, a_1, a_2..., a_n]
        :except
            * A lot of exceptions
        NzCoefficient list is None.r   zCoefficient list is empty.r	   z$Coefficients are not list of floats.)
r   �type�dictr
   �keys�list�max�range�_CoefficientsList�_Deg)�selfr$   �lst�pow_maxr   r   r   r   r   �__init__P   s*    		zPolynomial.__init__)r   �dervc             C   sN   | d k  s | |  j  k r' t d � � g  } | t k r= d St |  j � d S)aD  
            returns the value evaluated at p, or a list of value.
        :param p: point or points that evaluate the function at.
        :param derv: The depth of derivative for this polynomials you also want while evaluating it at p.
        :return:
            if derv = 0, then it will return the value of polynomial evaluated at a point or a list of points.
            else
                it will return a list of list where the first list is the 0th derivative, second list is the first.
                etc
            it will always return a list of numbers.
        r   z$Derivative for Polynomial not Valid.Nr	   r   )r,   r   r(   r   r+   )r-   r   r1   �resr   r   r   �eval_aty   s    zPolynomial.eval_at)r   �poly�	remainderc             C   sL   t  |  j | � } | r. t | d d � � n | } | rH | | d f S| S)aI  
            return q(x) such that p(x) = q(x)(x - b) + R, where R is a constant.
        :param b:
        :param poly:
        :param remainder:
        :return:
            (q(x)|[a_0, a_1, ...], R) if both is required
            q(x) or coefficents of q(x) depends on poly.
            R: The remainder if required.
        Nr	   r   r   )r   r+   r#   )r-   r   r4   r5   Znewcoefficientsr   r   r   r   �
factor_out�   s
    "zPolynomial.factor_outc             C   s�   d t  |  j � d } d } xp |  j D]e } | d k r� |  j | } | d t  | � d | d k rv d t  | � n d d 7} | d	 7} q' W| d d k r� | S| d  d � S)N�p_z(x) = r   �(�)z*x**� z + r	   �   �+�   ����������)�strr,   r+   )r-   r2   �counterr   Zx_powerr   r   r   �__repr__�   s    <zPolynomial.__repr__N)�__name__�
__module__�__qualname__�__doc__r   r   �int�Numberr   r0   �Vectorr3   �boolr6   rB   r   r   r   r   r#   K   s
   -)"r#   �__main__r	   r;   r   r=   r   r   �   zFactoring out (x - 0)N)rF   �typingr   r   r   �floatrG   �complexrH   rI   r   r   r   r"   r#   rC   �printr@   r   r+   r6   r   r   r   r   �<module>   s0   
)
_"...


