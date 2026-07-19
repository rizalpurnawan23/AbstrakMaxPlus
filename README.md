<p align="center">
    <img
    src= "img\abstrak_maxplus_logo.svg"
    alt= "AbstrakMaxPlus logo"
    style= "width: 50%; height: auto"
    >
</p>


# AbstrakMaxPlus

An intuitive, vectorized infix-notation module for basic Max-Plus algebra computations, built as part of the **Abstrak** computational mathematics ecosystem.

By replacing nested function calls with elegant infix operators, `AbstrakMaxPlus` allows you to write Python code that directly mirrors classical semiring literature notation.


## 📖 Mathematical Foundation

The Max-Plus algebra is an idempotent semiring $(\mathbb{R} \cup \{-\infty\}, \oplus, \otimes)$, where:
*   **Addition ($\oplus$):** $x \oplus y = \max(x, y)$
*   **Multiplication ($\otimes$):** $x \otimes y = x + y$

For matrices $A, B \in \mathbb{R}^{m \times n}$ and $C \in \mathbb{R}^{n \times p}$, these operations extend element-wise and vectorially:
*   **Matrix Addition ($A \oplus B$):** 
    $$(A \oplus B)_{ij} = \max(A_{ij}, B_{ij})$$
*   **Matrix Multiplication ($A \otimes C$):** 
    $$(A \otimes C)_{ij} = \bigoplus_{k=1}^n (A_{ik} \otimes C_{kj}) = \max_{k} (A_{ik} + C_{kj})$$


## ⚡ Key Features

### General Features

*   **Infix Notation:** Write expressions like `A |op| B` directly, eliminating the need for deeply nested function calls.
*   **Vectorized with NumPy:** Highly optimized operations exploiting C-level speeds for intensive evaluations.
*   **Mathematical Cleanliness:** Built to feel identical to blackboard or journal paper mathematics.

### Algorithmic Optimization

Unlike naive loop-based implementations that scale linearly, `AbstrakMaxPlus` implements **binary exponentiation by squaring** adapted for the max-plus semiring. Because max-plus matrix multiplication is associative, the matrix power $A^{\otimes(n)}$ is computed in $O(\log n)$ matrix multiplications using the following recursive structure:

$$
    A^{\otimes(n)} =
    \begin{cases}
        \left( A^{\otimes(2)} \right)^{\otimes (n/2)}
        &: 2 \mid n
        \\
        A \otimes (A^{\otimes 2})^{\otimes ((n-1)/2)}
        &: 2 \nmid n
    \end{cases}
$$

When combined with NumPy's underlying C-level vectorization, this ensures that large-scale state transitions and truncated Kleene-star computations scale efficiently for intensive evaluations.


## 🚀 Installation

You can install `AbstrakMaxPlus` directly from GitHub using `pip`:

```bash
pip install git+https://github.com/rizalpurnawan23/AbstrakMaxPlus.git
```

## 🛠️ Quick Start

Using the package is incredibly clean. Simply use the wild-card import to unleash textbook-ready notation directly in your environment:

```python
import numpy as np
from abstrak_maxplus import *

# Initialize some matrices (using real numbers)
# It is worth noting that we override E with -inf,
# the zero element of a max-plus semiring
A = randomMAT(3, 3, low= -10, high= 10, integers= True)
B = randomMAT(3, 3, low= -10, high= 10, integers= True)

# Identity matrix (0s on diagonal, -inf elsewhere)
I = idMAT(3)

print("Matrix A:")
print(A)
print("Matrix B:")
print(B)

# 1. Max-Plus Matrix Addition (A ⊕ B)
# Equivalent to element-wise maximum
C = A |op| B
print("\nAddition (A |op| B):")
print(C)

# 2. Max-Plus Matrix Multiplication (A ⊗ B)
# Equivalent to state-transition/path finding update
D = A |ot| B
print("\nMultiplication (A |ot| B):")
print(D)

# 3. Multiplying with Identity
# I |ot| A should equal A
print("\nI |ot| A = A -->", np.array_equal(I |ot| A, A))

# 4. Matrix exponentiation
print("\nExponentiation (A |exp| 11):")
print(A |exp| 11)

# 5. Truncated Kleene-star
print("\nTruncated Kleene-star (A |ast| 11):")
print(A |ast| 11)

# 6. Hadamard product
print("\nHadamard Product (A |od| B):")
print(A |od| B)

```

## 🧪 Included Operators Reference

- `|op|` ($\oplus$): Max-plus binary addition (element-wise maximum).
- `|ot|` ($\otimes$): Max-plus multiplication. If applied to matrices or matrix-vector, it functions as matrix multiplication.
- `|od|` ($\odot$): Hadamard (element-wise) max-plus product.
- `|ast|`: Truncated Kleene-star. Given a matrix $A$ and $n \in \mathbb{N}$, `A |ast| n` is the code for $A^{\ast(n)}$. It is also compatible if $A$ is a max-plus scalar.
- `|exp|`: Max-plus exponentiation. Given a matrix $A$ and $n \in \mathbb{N}$, `A |exp| n` is the code for $A^{\otimes(n)}$. It is also compatible if $A$ is a max-plus scalar.

## 📝 License

<!-- The source code of this project is open-source and licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details. -->
This project is open-source and licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.
