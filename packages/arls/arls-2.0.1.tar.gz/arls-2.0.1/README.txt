ARLS: Automatically Regularized Linear System Solver (Revised)

ARLS is intended for use in solving linear systems, Ax=b, which other solvers 
may not be able to handle. Ill-conditioning is the usual reason for people to seek
alternative solvers such as this. ARLS also has a rich set of constraints.

All these solvers apply to any shape of the matrix, A. That is, the 
system can have more rows than columns (over-determined), or the same number
of rows and columns (square), or fewer rows than columns (under-determined). 
And the matix A can be full rank, or have near zero singular values, 
or exactly zero singular values of any number.

Please see the in-code comments for details of calls and returns, 
including example applications for each routine.

Our primary solver is:
    x = arls(A, b)

If you need to solve many systems with the same matrix, A, but different b vectors, use:
    x = arlsusv(b, U, S, Vt)
where U, S, and Vt are the singular value decomposition of A, from:
    U, S, Vt = np.linalg.svd(A, full_matrices=False)

If you need to add constraint equations which must be satisfied exactly 
(such as "the sum of the solution elements must be 100.0") 
then put those equation in a separate system, Ex == f and call:
    x = arlseq(A, b, E, f)

If you need to add inequality constraints, such as "x1 + x2 >= 1.0" then 
put those equations in a separate system, Gx >= h and call:
    x = arlsgt(A, b, G, h)
For "<=" constraints you need to multiply both sides by -1.0 to convert
the constraint to a ">=" constraint.
    
If you need both equality and inequality constraints, use
    x =arlsall(A, b, E, f, G, h) 

While you can require many different types of constraints using the above,
we offer three special cases routines which are more efficient and robust 
and precise than using general constraints above:

    If you know the solution should be non-negative, use:
        x = arlsnn(A, b)
    If you know the solution should be non-decreasing ("rising") then use:
        x = arlsrise(A, b)
    If you know the solution should be non-increasing ("falling") then use:
        x = arlsfall(A, b)

    



