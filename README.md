## Project Description
    Using Newton's iteration to create newton's fractrals. 
## Dependencies
- [PyPng](https://github.com/drj11/pypng)
 
## Design Guidelines
- ### Core_modules/*
    - Everything has been implemented. The evaluation of the the polynomials is using nested multiplications which allows evaluations of the polynomials at the points, factoring the polynomials for roots finding, and evaluating its taylor coefficients at the point being evaluated. 
- ### faithful_newton.py
    1. Find all roots and their multiplicity for any given polynomials. 
    2. Label the roots with integers (An representative). 
    3. Perform faithful Newton Raphson iterations and identify which roots it's converging too. 
    4. Identify bad initial guess that leads to numerical errors.
    5. Keep tracks of the number of iterations too.  
 
## Problems: 
1. Slow convergence rate and bad accuracy for repeated roots 
from the polynomials. 
    * Solution using the derivative of the fixed point iteration function 
    near the region of the roots has been implemented. It's a lot of math
    hence details won't be written here. 
2. Bad initial guess identifier is preventing the convergence of repeated roots. 
    * Causes: 
        * For repeated roots, derivative of p(x) is clse to zero, which is misidentified as a bad initial guess, causing the loop to reset the initial guess value. 
    * solution: 
        * ~~Changes the conditions for bad initial guess~~? 
        * ~~Only test the very first guess intead of testing all guesses in the interation~~.
        * Test at the end of the fixed point iteration, if p(x_final) is not small enough or x_final blown up, then try again with a new guess with a larger interval for the initial guess.  
3. How to expand the root form of a polynomial into the regular form? 
    * Interpolation, but we need one extra points other than the roots to make it, interpolation is easy because we can just use the numpy module. 
4. [URGENT] For repeated roots, there is a chance the roots are slightly off, could be a result that the algorithm didn't detect the existence of repeated root during the Newton Iteration. 
   
    
        
## Potential Challenges: 
1. **Smooth graphics of the fractals can be very hard to attain, Potential solution**
    * Random sampling and Monte Carlo Algorithms for fractals evalutions
    * Post processing of the images using some python modules. 
2. **Repeating roots and roots that are very close to each other numerically**
    * Repeating roots sometimes are badly conditioned, causing Newton's method to converge to value that are slightly off from the roots founded from the roots finder. 
    * Roots very close to each other will create a very strict identifying conditions for knowing which root our initial guess converges to. 
3. **Truncation Errors in polynomial evaluation** 
    * Ill-conditioned polynomial might have error up to 1e-2 due to high degree of power, this is especially true for polynomials in the form of p(x) = (x - a)^n q(x) where n is larger than 10. This will create problem when identifying the 
    roots. 
        * Solution: 
        * The problem has been addressed with an ExtremeSolver class, the class perform multiple solves on the same polynomials, then it take the average for each of the roots together produce a standard deviation for the roots. Then, the roots is used to evaluate the value of the polynomial in roots product form, increasing the precision dramatically. 
        
        
        
## Other stuff
    * Why the fuck I cannot use my python virtual environment on my freaking desktop?!
    - 