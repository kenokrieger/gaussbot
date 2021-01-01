from sympy import symbols, Integral, preview, sin, latex

x, a, b, c = symbols('x a b c')
expr = Integral(sin(x), (x, a, b))
print(latex(expr))
# WHY IS PREVIEW NOT WORKING
