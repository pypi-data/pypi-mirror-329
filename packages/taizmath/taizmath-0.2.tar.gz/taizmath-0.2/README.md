
# taizmath

**taizmath** is an easy-to-use symbolic math library designed as an alternative to SymPy. It simplifies complex mathematical operations like differentiation, integration, Laplace transforms, Fourier transforms, and more.

## Features

- ✅ Symbolic algebra (`add`, `subtract`, `multiply`, `divide`)
- ✅ Calculus operations (`differentiate`, `integrate`)
- ✅ Transforms (`laplace`, `fourier`)
- ✅ Predefined constants (`pi`, `e`)
- ✅ Simple and intuitive syntax

## Installation

Install taizmath via pip:

pip install taizmath


## Usage

```python
from taizmath.core import Symbol
from taizmath.algebra import add
from taizmath.calculus import diff, integrate
from taizmath.transforms import laplace

x = Symbol('x')

# Algebraic operation
expr = add(x, 2)  # (x + 2)
print(expr)

# Differentiation
dx = diff(x, x)  # 1
print(dx)

# Integration
int_expr = integrate(x, x)  # x^2/2
print(int_expr)

# Laplace Transform
laplace_x = laplace(x)  # L[x]
print(laplace_x)
```
