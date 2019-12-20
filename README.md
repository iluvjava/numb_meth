## Project Description
    Using Newton's iteration to create newton's fractrals. 
## Dependencies
- [PyPng](https://github.com/drj11/pypng)
 
## Design Guidelines
- ### Core_modules/*
    - Everything has been implemented. The evaluation of the the polynomials is using nested multiplications which allows evaluations of the polynomials at the points, factoring the polynomials for roots finding, and evaluating its taylor coefficients at the point being evaluated. 
- ### faithful_newton.py
    1. Find all roots and their multiplicity for any given polynomials. 
    2. Label the roots with integers. 
    3. Perform faithful Newton Raphson iterations and identify which roots it's converging too. 
    4. Identify bad initial guess that leads to numerical errors.
    5. Keep tracks of the number of iterations too.  
 
## Problems: 
    1. Slow convergence rate and bad accuracy for repeated roots 
    from the polynomials. 
        * Solution using the derivative of the fixed point iteration function 
        near the region of the roots has been implemented. It's a lot of math
        hence details won't be written here. 
        
        
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
        
## Other stuff
    * Why the fuck I cannot use my python virtual environment on my freaking desktop?!
    - 