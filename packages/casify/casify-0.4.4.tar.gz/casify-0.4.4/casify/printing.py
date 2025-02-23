def pretty(expr):
    """Pretty print a symbolic expression."""
    import sympy

    expr = expr.replace(":", " =")
    expr = expr.replace("{", "")
    expr = expr.replace("}", "")
    expr = expr.replace(",", " ∧")

    return sympy.pretty(expr)
