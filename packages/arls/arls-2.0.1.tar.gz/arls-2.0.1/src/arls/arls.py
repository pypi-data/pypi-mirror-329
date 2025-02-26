"""
Copyright (c) 2024 Rondall E. Jones, Ph.D.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

(MIT License)

VERSION 2.0.1
This version inserts a missing line of code in arlsusvlamb,
shown here as the middle line of three lines.

    # process failed to find a useable lambda
    A = (U @ np.diag(S)) @ Vt
    return lstsq(A,b)[0],0.0

PURPOSE--------------------

Arls 2 is an upgrade to the Arls 1.0 package which has been available
since 2021 on the Python contributed library.

Arls (or ARLS, or arls) is a package for automatically solving
difficult (i.e., ill-conditioned or singular) linear systems of equations.
It also contains a rich set of constrained solvers which build
on the automatic solvers.

The main difference between Arls 1.0 and Arls 2.0 is that Arls 1.0 required 
many heuristic values in order to locate the unwanted rise in 
the Picard Condition Vector. (See technical discuss below.) 
But Arls 2.0 is focused on directly forcing the Picard Condition Vector
to decline by adjusting the Tikhonov regularization parameter.
Thus Arls 2.0 is fundamentally simpler and requires almost no
heuristics and also fewer helper routines.
We have also simplified some of the constrained solvers.

See OUR SOLUTION METHOD below.

USAGE SUMMARY--------------------------------------------

The calls available to the user are:

x = arls(A,b)
x = arlsusv(b,U,S,Vt)     (to reuse the SVD of A for efficiency)
x = arlseq(A,b,E,f)       (for equality constraints)
x = arlsgt(A,b,G,h)       (for inequality constraints)
x = arlsall(A,b,E,f,G,h)  (for both types of constraints)
x = arlsnn(A,b)           (for nonnegativity)
x = arlsrise(A,b)         (to force a non-decreasing solution)
x = arlsfall(A,b)         (to force a non-increasing solution)

USAGE DETAILS----------------------------------------------

(1) Suppose you have a system of equations to solve, Ax=b.
To use arls(), A does not have to be square. It can be any shape.
Then you can get our automatically regularized solution with the call
   x = arls(A, b)
Of course, if the system is well behaved, solution will be easy
and the answer will then be the same as any good solver would produce.

(2) If you want to efficiently solve many systems of equations with the 
same matrix A but different b vectors, 
first compute the Singular Value Decomposition like this:
   U, S, Vt = np.linalg.svd(A, full_matrices=False)
Then get the solution for Ax=b for a particular b by calling:
   x = arlsusv(b, U, S, Vt)

(3) Suppose you have special constraints you wish to obeyed exactly.
For example, you may want the solution values to add to 100.
Then form these "equality constraint" equations into a separate
linear system,
   Ex == f
and call
   x = arlseq(A, b, E, f)
There can be any number of such constraint equations.
But be careful that they make sense and do not conflict with each other
or arlseq() will have to delete some of the offending equations.

(4) Now, suppose you have "greater than" constraints you need the solution
to obey. For example, perhaps you know that none of the elements of x should
be less than 1.0. Then form these equations into a separate system,
   Gx >= h
and call
   x = arlsgt(A, b, G, h)
Of course, you can also have "less than" constraints, but you will need
to multiply such each equation by -1 (on both sides) to convert it to a
"greater than" constraint.

Note: if you only need the solution to be nonnegative, arlsnn() is
more efficient.

(5) The above two situations can be combined by calling
   x = arlsall(A, b, E, f, G, h)

(6) A common requirement is for the elements of x to all be non-negative.
To force this requirement on the solution, just call
   x = arlsnn(A, b)
(You still get all the benefits of automatic regularization.)

(7) Finally, if you know the solution should be non-decreasing
("rising") or non-increasing ("falling") then you can call
      x = arlsrise(A, b)
   or 
      x = arlsfall(A, b).
Obviously you could use arlsgt() with constraints requiring each x(i) 
to be greater than or equal to x(i-1). But arlsrise and arlsfall are 
very easy to call and also assure that flat portions of the solution
are exactly the same value.
         
Note: If A or b is empty or all zeros, an answer of all zeros
will be returned, regardless of the contents of E, f, G, or h.

Note: In regularizing ill-conditioned linear systems it is a good
idea to use as few constraints as possible, and to make them
the most insightful and natural to the situation as possible. 

Contact: rejones7@msn.com 

TECHNICAL DETAILS-------------------------------

    1. When Ax=b is ill-conditioned, the solution process works best 
       when the rows of A are scaled so that the elements of b 
       have similar estimated errors. However, this is NOT required.
    2. With any linear equation solver, you should check that each solution 
       is reasonable. In particular, you should check the residual vector, 
       Ax - b, or its norm, ||Ax - b||, or, equivalently, RMS(Ax - b) to
       be sure it is acceptable and appropriate for your problem.
    3. None of these routines needs or accepts parameters such as iteration
       limits, error estimates, variable bounds, condition number limits, etc.
    4. The intent of all routines in this module is to find a reasonable 
       solution even in the midst of excessive inaccuracy, ill-conditioning, 
       singularities, linear dependendies between rows, etc.
    5. In view of previous note, Arls is not appropriate for situations
       where the requirements are for high accuracy rather than
       robustness. So, we assume, in the coding, where needed, that 
       the data need not be considered more accurate than
       8 significant figures.

RAISES-----------------------------------------------

    LinAlgError:
        If A is not 2-D.
        If A is empty.
        If A and b do not have the same row size.
        If E is not 2-D.
        If E is empty.
        If E and f do not have the same row size.
        If G is not 2-D.
        If G is empty.
        If A and E do not have the same column size.
        If A and G do not have the same column size.
        If E and G do not have the same column size.
    In addition, SCIPY's SVD(), which is used by Arls,
    raises LinAlgError if it does not converge.

INTRODUCTORY EXAMPLE---------------------------------

Any linear system solver can handle easy problems.

For example, let
A = [[1, 2, 3],
     [1, 1, 1],
     [3, 2, 1]]
b = [6, 3, 6]

Then any linear equation solver will return:

x = [1, 1, 1]

But consider:

A = [[1, 2, 0],
     [1, 2, 0.01],
     [1.01, 2, 1]]
b = [3, 3.2, 3.9]

A quick look at these equations might lead one to think that the solution
will also be fairly close to all ones.
However, a naive solver will actually produce a shocking answer:
   y = [-1910.0, 956.5, 20.]
Arls(A,b) will see the instability and automatically regularize the
system to produce roughly
   z = [0.63, 1.24, 0.71] 
This is a massively better solution, though approximate.

Of course, there is a cost for adjusting the system in this fashion,
as A*z calculates to      [3.10, 3.11, 3.81]
rather then the desired b=[3.00, 3.20, 3.90].
There will generally be trade-offs like this when regularizing
such problems, whether manually or automatically.

Further, often one needs also to constraint the solution in some manner
such as requiring all solution values to be nonnegative.
(We offer several such variations).
However, the more one constrains the solution the more the resulting 
A*x values will tend to differ from the desired values in b.
This is behavior is fundamental, and not due to anything about 
the solution processes herein or elsewhere, or to our solvers
or any other solver's "fault".
 
EXAMPLE USE OF EQUALITY CONSTRAINTS---------------------------------------

Suppose the user is solving a small system of equations
for which the user knows that the correct sum of x must be 3:
     x + 2 y = 5.3   (Least Squares)
   2 x + 3 y = 7.8       "
       x + y = 3     ( Exact )
           
Then the arrays for arlseq are:

   A = [[ 1.,  2.0],
        [ 2.,  3.0]]
   b = [5.3, 7.8]
   
   E = [[ 1.0,  1.0]]
   f = [3.0]

The solution that arlseq(A,b,E,f) returns is [x,y] = [0.7, 2.3]
which satisfies x + y = 3 exactly,as requested.

EXAMPLE USE OF INEQUALITY CONSTRAINTS---------------------------------------   

Consider this small system of equations:
    A = [[1,1,1],
         [0,1,1],
         [1,0,1]]
    b = [5.9, 5.0, 3.9]

Any least-squares solver would produce x = [0.9, 2., 3.]
The residual for this solution is zero within roundoff.

But if we happen to know that all the answers should be at least 1.0
then we can add inequalites to insure that:
    x[0] >= 1
    x[1] >= 1
    x[2] >= 1

This can be expressed in the matrix equation Gx>=h where
    G = [[1,0,0],
         [0,1,0],
         [0,0,1]]
    h = [1,1,1]

Then arlsgt(A,b,G,h) produces x = [1., 2.035, 2.889].
The residual vector for this solution is [-0.015, -0.115, 0.028].

USE OF EQUALITY CONSTRAINTS AND INEQUALITY CONSTRAINTS-------------

If you happen to need both of the preceding types of contraints
then just call arls(A,b,E,f,G,h).

When adding complex constraints like this please take care that
all the constraints are consistent, both within the each type,
and between the two different types.
In the event of inconsistency between the equality constraints and
the inequality constraints, the equality constraints take precedence.

Note: An inequality constraint that asks for a variable to be
"greater than or equal to 0.0" may result in a value for
that variable of -1.0E-14 or so. This is in contrast to arlsnn(),
which guarantees the result will be absolutely non-negative.

EXAMPLE USE OF NONNEGATIVITY CONSTRAINTS---------------------------------------

Suppose we have this system to solve:
A = [[2,2,1],
     [2,1,0],
     [1,2,0]]
b = [3.9, 3, 2]

Most least squares solvers will return x = [1, 1, -0.1]
which solves the system exactly (within roundoff),
but has an unwanted negative value.
    
We can force a nonnegative answer with arlsnn, which returns
   x = [1.04, 0.92, 0.]
As is expected, this result has a non-zero residual,
which is [0.02, 0., -0.04]. 
This is to be expected.
    
OUR SOLUTION METHOD----------------------------------------------

Let us call the problem 
    A * x = b   (1)
and the represent the Singular Value Decomposition of A as 
    A = U * S * transpose(V) 
or briefly,
    A = U * S * Vt 
The pseudoinverse of S, called S+,  is defined by
    S+[i] = 1/S[i], unless S[i]==0, in which case S+[i]=0.0   
Then the slightly regularized solution to (1) is
    x= V * S+ * Transpose(U) * b      
which we represent as 
    x= V * PCV
where PCV= S+ * Ut * b is the so-called Picard Condition Vector.
Note that the PCV constitutes the coefficients of an orthogonal
expansion for x, with the columns of V being the orthogonal vectors.

The "Discrete Picard Condition" (or DPC), popularized by
Per Christian Hansen, simply says that the PCV should decline 
if a well conditioned solution is expected. 
If the PCV is not naturally declining, then the problem
should be regularized somehow to force the PCV
(or, rather, the so modified PCV) to decline.

In Arls we replace PCV by PCV(lambda) where lambda is a chosen
value of the Tikhonov regularization parameter.
Specifically, for a given value of lambda,
we replace S+ with S++, where 
    S++[i] = S[i]/(S[i]**2 + lambda**2)
(Note that if lambda=0.0, S++ is the same as S+.)
The resulting PCV(lambda) is then
    PCV(lambda) = S++ * Ut * b  (where S++ uses lambda)
And the regularized solution is
    x = V * PCV(lambda)

Arls does a fairly simple search for a value of lambda
which just barely causes a simple curve fit to the logarithm of
the PCV to decline. The use of the logarithm allows PCV values
near zero to be treated with as much significance as larger values.
A low-order curve fit is used to smooth out the
highly unpredictable values in the computed PCVs.

To avoid minor glitches in the solution we find with that process, 
we take the extra step of increasing lambda until the solution's 
residual increases by a factor of 1.5. 

REFERENCES and ACKNOWLEGEMENTS ---------------------------------

The auto-regularization algorithm in the original ARLS package
arose from the research for my dissertation, 
"Solving Linear Algebraic Systems Arising in the
Solution of Integral Equations of the First Kind", University of
New Mexico, Albuquerque, NM, 1985.

The algorithm used in this version resulted from the desire to
upgrade the algorithm in release 1.0 by avoiding so many heuristics
and replacing them with a direct application of the Picard Condition.

Many thanks to Cleve B. Moler, MatLab creater and co-founder of MathWorks,
for his kindness, energy, and insights in guiding my dissertation research.
My thanks also to Richard Hanson (deceased), co-author of the classic
"Solving Least Squares Problems", co-creater of BLAS, co-worker, and
co-advisor for the last year of my dissertation work.

The main reference for the Picard Condition is:
"The Discrete Picard Condition for Discrete Ill-posed Problems", 
by Per Christian Hansen, 1990.
More information at link.springer.com/article/10.1007/BF01933214

For discussion of incorporating equality and inequality constraints
(including nonnegativity) in solving linear algebraic problems, see
"Solving Least Squares Problems", by Charles L. Lawson and
Richard J. Hanson, Prentice-Hall 1974.
My implementation of these features has evolved somewhat
from that fine book, but is based on those algorithms.

Rondall E. Jones, Ph.D.
rejones7@msn.com
"""

from math import sqrt,log,log10,exp
import numpy as np
from numpy import atleast_1d, atleast_2d, absolute, cbrt
from scipy._lib._util import _asarray_validated
from scipy.linalg import LinAlgError
from scipy.linalg import lstsq
from scipy.linalg import norm

def checkAb(AA, bb):
    A = atleast_2d(_asarray_validated(AA, check_finite=True))
    b = atleast_1d(_asarray_validated(bb, check_finite=True))
    if len(A.shape) != 2:
        raise LinAlgError("Input array should be 2-D.")
    m, n = A.shape
    if m == 0 or n == 0:
        raise LinAlgError("Matrix is empty.")
    if len(b) != m:
        raise LinAlgError("Matrix and RHS do not have the same number of rows.")
    return A,b

def posratio(x):
    #Return the ratio of the element in x with the largest absolute value
    #to the element with the smallest non-zero absolute value.
    m=x.shape[0]
    ax=x
    for i in range(0,m): ax[i]=abs(x[i]) 
    xmax=max(ax)
    if xmax==0.0: return 0.0
    xmin=xmax
    for i in range(0,m):
        if ax[i]>0.0: xmin=min(xmin,ax[i])
    return xmax/xmin   
    
def worstof(G, h, x):
    # assess state of inequalities
    diff = G@x - h
    i=np.argmin(diff)
    if diff[i]>-0.00000001: return -1
    else: return i    

def fitline1(y):
    # compute straight line fit
    m=len(y)
    if m==1: return 0.0
    if m==2: return y[1]-y[0]
    A = np.zeros((m,2))     
    for i in range(0,m):
        xi = float(i)
        A[i,0] = xi 
        A[i,1] = 1.0
    coef = lstsq(A,y)[0]
    return coef[0] # return constant slope
     
def fitparab1(y):
    #compute parabola fit; y=ax^2 + bx +c, where x(i) = i
    m=len(y)
    if m==1: return 0.0
    if m==2: return y[1]-y[0]
    A = np.zeros((m,3))     
    for i in range(0,m):
        xi = float(i)
        A[i,0] = xi*xi # x^2 * a
        A[i,1] = xi    # x * b
        A[i,2] = 1     # 1 * c
    coef = lstsq(A,y)[0]
    a = coef[0]
    b = coef[1]
    #c = coef[2]
    #f = np.zeros(m)  # parabolic fit
    s = np.zeros(m)  # slope of that fit
    for i in range(0,m):
        xi = float(i)
        #f[i] = a*xi*xi + b*xi + c  # we don't actually need the fit...
        s[i] = 2.0*a*xi + b         # we just need its derivative
    return max(s) #return max slope
   
def arlsusvlamb(bb, U, S, Vt):
    #Determine a reasonable value for the Tikhonov lambda parameter
    V = np.transpose(Vt)
    Ut= np.transpose(U)
    b = atleast_1d(_asarray_validated(bb, check_finite=True))
    m = U.shape[0]
    n = V.shape[1]
    mg = min(m,n)
    if np.count_nonzero(S) == 0 \
    or np.count_nonzero(b) == 0 \
    or mg == 0: return np.zeros(n),0.0
    if m<3 or n<3 or posratio(S)<100.0: 
        A = (U @ np.diag(S)) @ Vt
        return lstsq(A,b)[0],0.0

    # Phase 1
    # setup
    sref = max(S)
    eps=sref*1.0E-9
    beta = Ut @ b
    for i in range(0, mg):
        if beta[i]==0.0: beta[i]=eps;  # do not change this
    g  = np.zeros(mg) # = S+ * Ut * b = PCV    
    ga = np.zeros(mg) # = abs(g)
    gg = np.zeros(mg) # = log10(gk)
    gok= np.zeros(mg) # save the ok solution
    gref = 0.0
    
    # main loop
    lamb = sref*1.0E-12
    lambprev = lamb
    lambok = 0.0
    ok = False
    factors=np.array([10.,2.,1.2,1.05])
    for ilamb in range(0,4):
        while lamb<sref:
            lambprev=lamb
            lamb=lamb*factors[ilamb]
            for i in range(0, mg):
                g[i] = beta[i] * (S[i] /(S[i]**2 + lamb**2))
            for i in range(0, mg):    
                ga[i] = abs(g[i])
            gref=max(ga[0],ga[1],eps)
            for i in range(0, mg):
                gg[i] = np.log10(max(ga[i]/gref , eps))
            s1=fitline1(gg)
            s2=fitparab1(gg)
            if min(s1,s2)<=0.0:
                ok=True
                gok=g.copy()
                lambok =lamb
                lamb=lambprev # backup one step to start next ilamb loop
                break        
        if not ok:
            # process failed to find a useable lambda
            A = (U @ np.diag(S)) @ Vt
            return lstsq(A,b)[0],0.0
        
    # solution for Phase 1
    x=np.transpose(Vt) @ g 
    Ax = U @ (np.diag(S) @ (Vt @ x))
    resid1=norm(Ax-b)

    # Phase 2: search for larger lambda that minimally increases norm(x)
    # using loosening factor of 1.5 not 2.0
    lamb =lambok
    while lamb<sref:
        lamb=lamb*1.2
        for i in range(0, mg):
            g[i]  = beta[i] * (S[i] /(S[i]**2 + lamb**2))
        x=np.transpose(Vt) @ g
        Ax = U @ (np.diag(S) @ (Vt @ x))
        resid=norm(Ax-b)
        if resid>1.5*resid1: break
    return x,lambok

def arlsusv(b, U, S, Vt):
    x,lamb=arlsusvlamb(b, U, S, Vt)
    return x

def arls(AA, bb):
    A, b=checkAb(AA,bb)
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    x,lamb=arlsusvlamb(b, U, S, Vt)
    return x

def max_row_norm_of(A):
    # determine max row norm of A
    m = A.shape[0]
    rnmax = 0.0 
    for i in range(0, m):
        rn = norm(A[i, :])
        if rn > rnmax:
            rnmax = rn
    return rnmax

def max_sense_of(E, f):
    # find the row of Ex=f which his the highest ratio of f[i]
    # to the norm of the row.
    imax = 0
    smax = 0.0
    m = E.shape[0]
    for i in range(0, m):
        rn = norm(E[i, :])
        if rn > 0.0:
            s = abs(f[i]) / rn
            if s > smax:
                smax = s
                imax = i
    return imax, smax

def prepeq(EE, ff):
    #a utility routine for arlseq() that orthogonalizes the constraints
    E=EE.copy()
    f=ff.copy()
    m, n = E.shape
    if m==0 or np.count_nonzero(E)==0:
        return np.zeros((0,n)), np.zeros(0)
    if m==1:
        rn = norm(E[0,:])
        return E/rn, f/rn
    neglect = max_row_norm_of(E) * 0.00000001
    i=0
    while i<m: 
        # determine new best row
        if i == 0:
            imax,smax = max_sense_of(E, f)
        else: 
            rnmax = -1.0  
            imax = -1
            for k in range(i, m):
                rn = norm(E[k,:])  
                if rn > rnmax:
                    rnmax = rn
                    imax = k
        #check norm of new max row            
        rin = norm(E[imax,:])        
        if rin < neglect:
            E = np.delete(E, imax, 0)
            f = np.delete(f, imax, 0)
            m, n = E.shape  # row size decreases...
            continue
        # normalize
        rn = norm(E[imax,:])
        E[imax,:] /= rn
        f[imax] /= rn     
        # exchange rows
        if  i!=imax:
            E[[i, imax],:] = E[[imax, i],:]
            f[[i, imax]] = f[[imax, i]]
        # subtract projections onto row i
        for k in range(i+1, m):
            d = np.dot(E[k,:], E[i,:])
            E[k,:] -= d * E[i,:]
            f[k]   -= d * f[i]
        i+=1                # ... or number of good rows increases
    return E, f 

def arlspj(AA, bb, E, f):
    # subtract the projection of Ax=b onto Ex=f from Ax=b
    # making the two systems orthogonal
    A=AA.copy()
    b=bb.copy()
    ma, na = A.shape
    me, ne = E.shape
    rnmax = max_row_norm_of(A)
    if rnmax==0.0: return A,b
    neglect = rnmax * 0.00000001  
    i = 0
    while i < ma:
        for j in range(0, me):
            d = np.dot(A[i, :], E[j, :])
            A[i, :] -= d * E[j, :]
            b[i] -= d * f[j]
        nm = norm(A[i, :])
        if nm < neglect:
            A = np.delete(A, i, 0)
            b = np.delete(b, i, 0)
            ma, na = A.shape
        else:
            A[i, :] = A[i, :] / nm
            b[i] = b[i] / nm
            i += 1
    return A,b

def arlseq(AA, bb, EE, ff):
    A,b=checkAb(AA,bb)
    E,f=checkAb(EE,ff)
    m, n = A.shape
    me, ne = E.shape
    if n != ne: raise LinAlgError( \
        "The two matrices do not have the same number of unknowns.")
    if A.shape[0]==0:          return np.zeros(n)       
    if np.count_nonzero(A)==0: return np.zeros(n)
    if np.count_nonzero(b)==0: return np.zeros(n)
    if E.shape[0]==0:          return arls(A,b)
    if np.count_nonzero(E)==0: return arls(A,b)
    E, f = prepeq(E,f)
    if E.shape[0]<1: return arls(A,b)
    xe = np.transpose(E) @ f
    Ap,bp = arlspj(A,b,E,f)
    if Ap.shape[0]<1: return xe    
    xt = arls(Ap,bp)
    return xt + xe

def arlsgt(AA, bb, GG, hh):
    A,b=checkAb(AA,bb)
    G,h=checkAb(GG,hh)
    m, n = A.shape
    mg, ng = G.shape
    if n != ng:
        raise LinAlgError(
            "The two matrices do not have the same number of columns.")
    if np.count_nonzero(A) == 0 \
    or np.count_nonzero(b) == 0:
        return np.zeros(n)
    if np.count_nonzero(G) == 0: return arls(A,b)
    ng = G.shape[1]
    E = np.zeros((0, n))
    f = np.zeros(0)
    x = arls(A, b)
    # while constraints are not fully satisfied:
    for i in range(0,mg):
        p = worstof(G, h, x)
        if p<0: break
        row = G[p,:]
        rhsp = h[p]
        G = np.delete(G, p, 0)
        h = np.delete(h, p, 0)
        me = E.shape[0]
        if me == 0:
            E = np.zeros((1, n))
            E[0, :] = row
            f = np.zeros(1)
            f[0] = rhsp
        else:
            me += 1
            E = np.resize(E,(me, n))
            E[me - 1, :] = row[:]
            f = np.resize(f, me)
            f[me - 1] = rhsp
        # re-solve modified system
        x = arlseq(A, b, E, f)
    return x

def arlsall(AA, bb, EE, ff, GG, hh):
    A,b=checkAb(AA,bb)
    E,f=checkAb(EE,ff)
    G,h=checkAb(GG,hh)
    m, n = A.shape
    me, ne = E.shape
    mg, ng = G.shape
    if n!=ne or n!=ng:
        raise LinAlgError(
            "The matrices do not all have the same number of unknowns.")
    nzA = np.count_nonzero(A)
    nzb = np.count_nonzero(b)
    nzE = np.count_nonzero(E)
    nzG = np.count_nonzero(G)
    if nzA==0: return np.zeros(n)
    if nzb==0: return np.zeros(n)
    if nzE==0: return arlsgt(A,b,G,h)
    if nzG==0: return arlseq(A,b,E,f)
    E,f = prepeq(E,f)
    xe = np.transpose(E) @ f
    A,b = arlspj(A,b,E,f)
    G,h = arlspj(G,h,E,f)
    xt = arlsgt(A,b,G,h) 
    return xt+xe
    
def arlsnn(AA,bb):
    A,b=checkAb(AA,bb)
    m, n = A.shape
    if np.count_nonzero(A) == 0 or np.count_nonzero(b) == 0:
        return np.zeros(n)
    # get initial solution and Tikhonov parameter
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    xt, lambdah = arlsusvlamb(b, U, S, Vt)
    # see if unconstrained solution is already non-negative
    if min(xt) >= 0.0: return xt

    # the approach here is to actually delete columns,
    # for SVD speed and stability,
    # rather than just zero out columns.
    C = A.copy()
    cols = [0] * n  # list of active column numbers
    for i in range(1, n):
        cols[i] = i
    nn = n
    for i in range(1, nn):
        # choose a column to zero
        p = -1
        worst = 0.0
        for j in range(0, nn):
            if xt[j] < worst:
                p = j
                worst = xt[p]
        if p < 0:
            break
        # remove column p and resolve
        C = np.delete(C, p, 1)
        cols.pop(p)
        nn -= 1
        U, S, Vt = np.linalg.svd(C, full_matrices=False)
        ms = len(S)
        ps = np.zeros(ms)
        for i in range(0, ms):
            ps[i] = 1.0 / (S[i] + lambdah ** 2 / S[i]) if S[i] > 0.0 else 0.0
        xt = np.transpose(Vt) @ (np.diag(ps) @ (np.transpose(U) @ b))

    # degenerate case: nn==1
    if  xt[0] < 0.0:
        xt[0] = 0.0
    # rebuild full solution vector
    x = np.zeros(n)
    for j in range(0, nn):
        x[int(cols[j])] = xt[j]
    # double check to be sure solution is nonnegative
    for j in range(0, nn):
        x[j] = max(x[j], 0.0)
    return x

def worstdrop(x):
    # locate the worst violation of x to rise (or stay constant)
    n=x.shape[0]
    d=0.0
    dmin=0.0
    imin=-1
    i=0
    for i in range(1,n):
        d=x[i]-x[i-1]
        if d<dmin:    
            dmin=d
            imin=i
    return imin        

def arlsrise(AA, bb):
    # for forcing non-decreasing (aka rising) solution.
    A,b=checkAb(AA,bb)
    m,n=A.shape
    cols=[1]*n
    xt=np.zeros(n) 
    j=0
    # handle worst violation of rising constraint
    for k in range(0,n):
        xt = arls(A,b)
        j = worstdrop(xt)
        if j<0: break
        # absorb column j into columns j-1
        for i in range(0,m): A[i,j-1]+=A[i,j]
        A = np.delete(A, j, 1)
        cols[j-1]+=cols[j]; cols=np.delete(cols,j,0)
    # build final solution from compressed solution
    x=np.zeros(n)
    ix=0
    nc=len(cols)
    for j in range(0,nc):
        for k in range(0,cols[j]):
            x[ix]=xt[j]; ix+=1
    return x        

def arlsfall(A,b):
    # for forcing non-increasing (aka falling) solution.
    return -arlsrise(A,-b)
