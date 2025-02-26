# coverage test for arls.py
import numpy as np
from scipy.linalg import norm  
from scipy.linalg import lstsq  
from numpy.testing import assert_, assert_array_almost_equal_nulp

from arls import (
    arls,
    arlsusv,
    prepeq,
    arlseq,
    arlsgt,
    arlsnn,
    arlsall,
    arlsrise,
    arlsfall
)

def my_eye(m, n):
    A = np.zeros((m, n))
    for i in range(0, min(m,n)):
        A[i,i]=1.0
    return A

def myrandom(m,n):
    A = np.zeros((m,n))
    for i in range(0, m):
        for j in range(0, n):
            A[i,j] = abs(np.sin(float(2*m+3*n) + 2.0*float(i) + 2.5*float(j)))
    return A

def myhilbert(m, n):
    A = np.zeros((m, n))
    for i in range(0, m):
        for j in range(0, n):
            A[i, j] = 1.0/(1.0+i+j)
    return A

def myrandomerr(err, m):
    x = np.zeros(m)
    for i in range(0, m):
        x[i] = err * 0.5 * np.sin(4.0 * float(m + i))
    return x
    
def test_zero_rhs():
    # test solvers with zero right hand side
    A = np.eye(3)
    b = np.zeros(3)
    x = arls(A, b)
    assert_(norm(x) == 0.0, 
        "Solution of arls() is incorrectly non-zero.")
    x = arlseq(A, b, A, b)
    assert_(norm(x) == 0.0, 
        "Solution of arlseq() is incorrectly non-zero.")
    x = arlsgt(A, b, A, b)
    assert_(norm(x) == 0.0, 
        "Solution of arlsgt() is incorrectly non-zero.")
    x = arlsnn(A, b)
    assert_(norm(x) == 0.0, 
        "Solution of arlsnn() is incorrectly non-zero.")
    return
    

def test_regularization1():
    A = myhilbert(12,12)
    xx = np.ones(12)
    b = A @ xx
    for i in range(0, 12):
        b[i] += 0.00001 * np.sin(float(i + i))
    ans = np.array(
        [
            0.998635,
            1.013942,
            0.980540,
            0.986143,
            1.000395,
            1.011578,
            1.016739,
            1.015970,
            1.010249,
            1.000679,
            0.988241,
            0.973741,
        ]
    )
    x1 = arls(A, b)
    d = norm(ans - x1)
    assert_(d < 0.01*norm(ans), "Solution of arls() is not as expected.")
    return

def test_regularization2():
    # a typical problem
    n=6 
    A = myhilbert(n,n)
    ans= np.ones(n)
    b = A @ ans
    for i in range(0,n):
        b[i] += 0.00001 * np.sin(float(i + i))
    y = lstsq(A,b)[0]
    x = arls(A,b)
    d = norm(ans - x)
    #print("test2 reg, true ans=",ans)
    #print("test2 reg, naive ans=",y)
    #print("test2 reg, calc ans=",x)
    #print("d=",d)
    #print("norm(ans)=",norm(ans))
    assert_(d < 0.2*norm(ans), "Solution of arls() differs from normal.")
    return

# TEST ARLSEQ
def test_arlseq():
    n = 10
    A = np.eye(n)
    x = np.ones(n)
    x[3] = 5.0
    b = A @ x
    E = myhilbert(5,n)
    E[2,2] = 2.0
    E[3,3] = 3.0
    f = E @ x
    xx = arlseq(A, b, E, f)
    assert_(abs(xx[3] - 5.0) < 1.0e-4, "Constraint not obeyed in arlseq.")
    d = norm(x - xx)
    assert_(d < 0.01, "Residual too large in arsleq.")

    #test empty system
    E = np.zeros((3,3))
    f = np.zeros(3)
    E,f=prepeq(E,f)
    
    E = np.zeros((1,0))
    f = np.ones(1)
    E,f=prepeq(E,f)
    
    #test row interchange
    A = np.eye(3)
    b = np.ones(3)
    E = np.array([[1.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    f = np.array([2.0, 1.0, 2.0])
    ans = np.array([1.0, 1.0, 2.0])
    x = arlseq(A, b, E, f)
    
    d = norm(x-ans)
    assert_(d < 0.0001, "Solution of arlseq differs from normal.")

    #test row deletion
    E = np.eye(3)
    E[1,:]=E[2,:] # duplicate a row
    E = np.delete(E, 0, 0) # leave just the duplicates
    m1,n=E.shape
    f = np.array([1.,1.])
    E2,ff = prepeq(E, f)
    m2,n2=E2.shape
    assert(m2<m1,"Duplicate row not removed in prepeq.")
    return

# TEST ARLSGT
def test_arlsgt():
    x = np.array([6.0, 5.0, 4.0, 3.0])
    A = myhilbert(5,4)
    b = A @ x
    G = np.array([[0.0, 0.0, 0.0, 1.0]])
    h = np.array([5.0])
    xx = arlsgt(A, b, G, h)
    #print("in test_arlsgt")
    #print(xx.shape)
    #print(xx)
    assert_(abs(xx[3]-5.0) < 0.00001, "Arlsgt residual is too large.")
        
    A = np.array([[1.0, 1.0, 1.0], [0.0, 0.0, 0.0]])
    b = np.array([0.0, 1.0])
    G = np.eye(3)
    h = np.zeros(3)
    x = arlsgt(A, b, G, h)
    assert_(norm(x) == 0.0, "Solution by arlsgt should be zero.")
    return


# TEST ARLSALL
def test_arlsall():
    m = 8
    n = 7
    x = np.array([5.2, 4.0, 3.0, 2.0, 1.0, -1.0, -2.0])
    xsum = x.sum()
    A = myhilbert(m,m)
    A = np.delete(A, m - 1, 1)  # A is now 8 x 7

    b = A @ x
    for i in range(0, m):
        b[i] += 0.0001 * np.sin(float(2 * m + 2 * i))  # add noise

    E = np.zeros((2, n))
    f = np.zeros(2)
    E[0,2] = 1.0; f[0] = 3.0   #require xx[2]=3
    E[1,4] = 1.0; f[1] = 1.0   #require xx[4]=1

    G = my_eye(7,n)
    G = np.delete(G, 0, 0)     # redundant
    G = np.delete(G, 1, 0)     # redundant
    mg,ng=G.shape
    h = np.zeros(mg)           # require most x[i] to be nonnegative
    
    Z = np.zeros((1, n))       # zero arrays for dummies
    z = np.zeros(1) 

    # solve with with (A,-,-)
    xx = arlsall(A, b, Z, z, Z, z)
    d = abs(xx.sum() - xsum)
    assert_(d < 0.4, "In Arlsall, sum(x) is not as expected. (1)")

    # Solve with (A,E,-)
    xx = arlsall(A, b, E, f, Z, z)
    d = abs(xx.sum() - xsum)
    assert_(d < 0.01*xsum, "In Arlsall, sum(x) is not as expected. (2)")
    d = abs(xx[2] - 3.0)
    assert_(d < 0.0001,"In Arlsall, x[2] is not as expected. (3)")
    d = abs(xx[4] - 1.0)
    assert_(d < 0.0001,"In Arlsall, x[4] is not as expected. (4)")

    # Solve with (A,-,G)
    xx = arlsall(A, b, Z, z, G, h)
    assert_(min(xx)+0.00000001 >= 0.0, 
        "In Arlsall, x is not nonnegative. (5)")

    # Solve with (A,E,G)
    xx = arlsall(A, b, E, f, G, h)
    for i in range(0, 5):
        assert_(xx[i]>= 0.0,"In Arlsall, an x value is not nonnegative. (6)")
    d = abs(xx[2] - 3.0)
    assert_(d < 0.0001,"In Arlsall, x[2] is not as expected. (7)")
    d = abs(xx[4] - 1.0)
    assert_(d < 0.0001,"In Arlsall, x[4] is not as expected. (8)")
    return
    
# TEST ARLSNN
def test_arlsnn():
    A = np.ones((3, 1))
    b = np.array([1.0, 1.0, 1.0])
    x = arlsnn(A, b)
    assert_(x[0] == 1.0, "Arlsnn not handling single column right. (1)")
    
    A = np.eye(4)
    b = np.ones(4)
    x1 = arls(A,b)
    x2 = arlsnn(A,b)
    assert_(norm(x1-x2)<0.000001, 
        "Arlsnn not handling no-op right. (2)")

    # should produce all zero result
    A = np.eye(3)
    b = np.ones(3)
    for i in range(0,3): b[i]=-1.0
    x = arlsnn(A, b)
    assert_(norm(x) == 0.0, 
        "Solution of arlsnn is incorrectly non-zero. (3)")

    A = myhilbert(9,9) + 0.02 * myrandom(9, 9)
    m, n = A.shape
    ans = np.zeros(n)
    for i in range(0, n):
        ans[i] = i - 1
    b = A @ ans
    x = arlsnn(A, b)
    assert_(
        np.count_nonzero(x) >= 3
        and norm(A @ x - b) < 0.4
        and abs(x.sum() - ans.sum()) < 1.0,
            "Solution of arlsnn has changed (4)")
    return


# TEST ARLS shapes
def test_arlsrise():
    m = 15
    n = m
    A = myhilbert(m,m)
    xrand = myrandomerr(0.05, n)
    x1 = np.zeros(n)
    for i in range(0, n):  # create noisy func similar to y=x^2
        x1[i] = xrand[i] + 2.5 * float(i * i) / float(n * n) - 0.2
    tol = 0.0001
    b = A @ x1
    x = arlsrise(A,b)
    f = 0
    for i in range(0, n - 1):
        if x[i + 1] - x[i] < -tol:
            f = f + 1
    assert_(f == 0, "Arlsrise(A,b) failed.")

    for i in range(0, n):
        x1[i] = -x1[i]
    b = A @ x1
    x = arlsfall(A, b,)
    f = 0
    for i in range(0, n - 1):
        if x[i + 1] - x[i] > tol:
            f = f + 1
    assert_(f == 0, "Arlsfall(A,b) failed.")
    return

      

