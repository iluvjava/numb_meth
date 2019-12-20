## Project Description
    
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
    1. Smooth graphics of the fractals can be very hard to attain, but here are some potential solutions: 
        * Random sampling and Monte Carlo Algorithms for fractals evalutions
        * Post processing of the images using some python modules. 
