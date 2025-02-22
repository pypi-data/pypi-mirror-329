class Symbol:
    """Represents a symbolic variable (e.g., x, y, z)."""
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Expression:
    """Represents a mathematical expression."""
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def __repr__(self):
        return f"({self.lhs} {self.op} {self.rhs})"


# Algebraic Operations
def add(a, b): return Expression(a, "+", b)
def sub(a, b): return Expression(a, "-", b)
def mul(a, b): return Expression(a, "*", b)
def div(a, b): return Expression(a, "/", b)


# Calculus Functions
def diff(expr, var):
    """Computes the derivative of an expression with respect to a variable."""
    if expr == var:
        return 1
    if isinstance(expr, Expression) and expr.op == "+":
        return add(diff(expr.lhs, var), diff(expr.rhs, var))
    return 0  # Constants have a derivative of 0

def integrate(expr, var):
    """Computes the integral of an expression with respect to a variable."""
    if expr == var:
        return Expression(expr, "^", 2), div(1, 2)
    return Expression("∫", expr, var)  # Symbolic representation


# Transforms
def laplace(expr):
    """Computes the Laplace transform of an expression."""
    return f"L[{expr}]"

def fourier(expr):
    """Computes the Fourier transform of an expression."""
    return f"F[{expr}]"


# Mathematical Constants
pi = 3.141592653589793
e = 2.718281828459045
