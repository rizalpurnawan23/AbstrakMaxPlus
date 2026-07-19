# -------------------------------------------------------------------
# PYTHON MODULES IN USE
import numpy as np
import time
from functools import reduce

## -------------------------------------------------------------
## PRELIMINARY SETTING
# Infix with Numpy
class InfixBind:
    # Forces NumPy to yield control on the right
    # side (proxy | B)
    __array_ufunc__ = None 

    def __init__(self, func, left):
        self.func = func
        self.left = left

    def __or__(self, right):
        return self.func(self.left, right)
        
class Infix:
    # Forces NumPy to yield control on the left
    # side (A | proxy)
    __array_ufunc__ = None 

    def __init__(self, func):
        self.func = func

    def __ror__(self, left):
        return InfixBind(self.func, left)
        

# For random numbers generation
rng = np.random.default_rng()
    
# E = 'E'     # Oplus identity
E = float("-inf")


## -------------------------------------------------------------
## IDENTITY AND ZERO MATRICES
def idMAT(n:int):
    In = np.full((n, n), E)
    np.fill_diagonal(In, 0)
    return In

def null(n:int):
    return np.full((n, n), E)


## -------------------------------------------------------------
## RANDOM MATRIX
def randomMAT(
        m:int, n:int,
        low= None, high= None,
        integers= False
        ):
    if integers == True:
        if low is None:
            low = 0
        if high is None:
            high= 1000
    return rng.random((m, n)) if integers == False \
        else rng.integers(low= low, high= high, size= (m, n))


## -------------------------------------------------------------
## BINARY AND n-ARY ⊕
@Infix
def op(a: int | float, b: int | float | np.ndarray):
    if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
        if a.shape != b.shape:
            raise ValueError
    return np.maximum(a, b)

def osum(li: list):
    if not li:
        return E
    return np.max(np.array(li), axis= 0)


## -------------------------------------------------------------
## BINARY AND n-ARY ⊗
def _mat_ot(A, B):
    B_1d = B.ndim == 1
    B_col = B[:, np.newaxis] if B_1d else B
    result = np.max(
        A[:, :, np.newaxis] 
        + B_col[np.newaxis, :, :], axis= 1
        )
    return result[:, 0] if B_1d else result

@Infix
def ot(
        a: int | float | np.ndarray,
        b: int | float | np.ndarray
        ):
    # For matrix multiplication:
    if (isinstance(a, np.ndarray) \
            and isinstance(b, np.ndarray)):
        return _mat_ot(a, b)
    # For scalars:
    return a + b

def oprod(li: list, verbose= False):
    if not li:
        return 0
    if isinstance(li[0], np.ndarray):
        st = time.time()
        result = reduce(_mat_ot, li)
        en = time.time()
        if verbose == True:
            print(f"Runtime: {round(en - st, 3)} sec")
        return result
    return np.sum(li)


## -------------------------------------------------------------
## HADAMARD PRODUCT ⊙
@Infix
def od(
        a: int | float | np.ndarray,
        b: int | float | np.ndarray
        ):
    return a + b

def ohprod(li: list):
    if not li:
        return 0
    return np.sum(li, axis= 0)


## -------------------------------------------------------------
## EXPONENTIATION
def _exp(a, n, verbose= False):
    # For scalars:
    if not (isinstance(a, np.ndarray)):
        return n *a
    dim = a.shape[0]
    an = idMAT(dim)
    base = a.copy()
    st = time.time()
    while n > 0:
        if n % 2 == 1:
            an = _mat_ot(an, base)
        n //= 2
        if n == 0:
            break
        base = _mat_ot(base, base)
    en = time.time()
    if verbose == True:
        print(f"Runtime: {round(en - st, 5)} sec")
    return an

@Infix
def exp(a: int | float | np.ndarray, n: int):
    return _exp(a, n)


## -------------------------------------------------------------
## KLEENE-STAR
def _ast(A, n, verbose= False):
    dim = A.shape[0]
    I = idMAT(dim)
    p = int(n -1)
    B = _exp(I |op| A, p, verbose= verbose)
    return B

@Infix
def ast(A: int | float | np.ndarray, n: int):
    return _ast(A, n)
