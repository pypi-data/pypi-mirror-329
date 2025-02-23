# import sympy
# import sys


def _get_func(expr):
    import re

    match = re.match(r"(\w+)\((-?\w+|-?\d+)\)", expr.strip())
    if match:
        func_name, arg = match.groups()
        return func_name, arg
    else:
        return False, False


def _handle_expression(expr):
    known_functions = [
        "cos",
        "sin",
        "tan",
        "exp",
        "acos",
        "asin",
        "atan",
        "log",
        "log2",
        "log10",
    ]

    func_name, arg = _get_func(expr)
    if func_name:
        if func_name in known_functions:
            import sympy

            return sympy.sympify(expr)
        else:
            import sys

            main_module = sys.modules["__main__"]
            main_globals = main_module.__dict__
            func = main_globals.get(func_name)

            return func(arg)
    else:
        import sympy

        return sympy.sympify(expr)


def reorder_solution(solution):
    """Reorder terms so negative bounds appear before positive ones"""
    if "∨" not in solution:
        return solution

    # Split into OR terms and strip whitespace
    terms = [t.strip() for t in solution.split("∨")]

    # Helper to check if term contains negative number
    def has_negative(term):
        return "-" in term and any(c.isdigit() for c in term)

    # Sort terms - negative bounds first
    sorted_terms = sorted(terms, key=lambda x: (0 if has_negative(x) else 1))

    return " ∨ ".join(sorted_terms)


def is_redundant_bound(expr):
    import sympy
    from sympy import Symbol, oo

    """Check if expression is a redundant bound like (-oo < x) or (x < oo)"""
    x = Symbol("x")
    return isinstance(expr, sympy.core.relational.Relational) and (
        (expr.lhs == x and expr.rhs == oo)
        or (expr.lhs == -oo and expr.rhs == x)
        or (expr.lhs == x and expr.rhs == -oo)
        or (expr.rhs == x and expr.lhs == oo)
    )


def ast_simplify_inequalities(expr):
    from sympy import And, Or, Symbol

    x = Symbol("x")

    # Base case: if expression is atomic or doesn't need simplification
    if not isinstance(expr, (And, Or)):
        return expr

    if isinstance(expr, And):
        # Filter out redundant bounds and simplify remaining terms
        terms = [
            ast_simplify_inequalities(term)
            for term in expr.args
            if not is_redundant_bound(term)
        ]

        # If no terms left after filtering, return original expression
        if not terms:
            return expr

        # If only one term left, return it directly
        if len(terms) == 1:
            return terms[0]

        # Rebuild And expression with simplified terms
        return And(*terms)

    if isinstance(expr, Or):
        # Simplify each term in the Or expression
        terms = [ast_simplify_inequalities(term) for term in expr.args]

        # Sort terms to put negative bounds first
        def sort_key(term):
            # Helper to determine if term represents x < negative_number
            if isinstance(term, sympy.core.relational.StrictLessThan):
                if term.lhs == x and term.rhs.is_number:
                    return (0, float(term.rhs))
            return (1, 0)  # Default sort position for other terms

        sorted_terms = sorted(terms, key=sort_key)
        return Or(*sorted_terms)

    return expr


def replace_special_cases(solution):
    solution = solution.replace("-∞ < x ∧ x < ∞", "x ∈ ℝ")
    solution = solution.replace("False", "x ∈ ∅")

    return solution


def simplify_solution(solution_str):
    import sympy

    try:
        # Convert string to Sympy expression
        expr = sympy.sympify(solution_str)
        # Transform AST to remove redundant constraints
        expr_simpl = ast_simplify_inequalities(expr)
        # Convert to pretty string with unicode
        try:
            expr_simpl = sympy.pretty(expr_simpl, use_unicode=True)
        except UnicodeEncodeError:
            expr_simpl = sympy.pretty(expr_simpl)

        expr_simpl = replace_special_cases(expr_simpl)

        expr_simpl = reorder_solution(expr_simpl)

        return expr_simpl
    except Exception as e:
        print(f"Error processing solution: {e}")
        return solution_str


def solve(*equations, variables=None, pprint=True):
    """Solves an equation or a set of equations or inequalities.

    Args:
        *equations (str): a variable number of strings representing equations or inequalities.
        pprint (bool): Gives a mathematical-like output. Defaults to `True`.

    Returns:
        str or list: A string representation of the solutions if pprint is True, otherwise a list of dictionaries containing the solutions. Return "No solution" if no real solutions are found.

    Examples:
        >>> from casify import *
        >>> solve("x**2 - x - 6 = 0")
        'x = -2    ∨    x = 3'
        >>> solve("x + y - z = 1", "x + y + 2*z = 3", "-x + y + z = -1")
        'x = 5/3 ∧ y = 0 ∧ z = 2/3'
        >>> f = function("a * x**2 + b*x + c")
        >>> solve("f(1) = 2", "f(-1) = 3", "f(3) = 4")
        'a = 3/8 ∧ b = -1/2 ∧ c = 17/8'

    """
    import sympy

    eqs = []
    # Parse the equations
    for eq in equations:
        if ">" in eq or "<" in eq:
            if ">=" in eq:
                lhs, rhs = eq.split(">=")
                sign = ">="

            elif "<=" in eq:
                lhs, rhs = eq.split("<=")
                sign = "<="

            elif ">" in eq:
                lhs, rhs = eq.split(">")
                sign = ">"

            elif "<" in eq:
                lhs, rhs = eq.split("<")
                sign = "<"

            lhs = _handle_expression(lhs)
            rhs = _handle_expression(rhs)
            eq = " ".join([str(lhs), sign, str(rhs)])

            return _solve_inequality(eq)

        else:
            if "==" in eq:
                lhs, rhs = eq.split("==")

            elif "=" in eq:
                lhs, rhs = eq.split("=")

            lhs = _handle_expression(lhs)
            rhs = _handle_expression(rhs)

            eqs.append(sympy.Eq(lhs, rhs))

    if variables:
        solutions = sympy.solve(eqs, variables, dict=True)
    else:
        solutions = sympy.solve(eqs, dict=True)

    # Remove complex solutions from the solution set.
    real_solutions = []
    if isinstance(solutions, dict):
        real_solutions = {
            key: solutions.get(key) for key in solutions if solutions.get(key).is_real
        }
        real_solutions = [real_solutions]
        real_solutions = [sol.get(key) for key in real_solutions if not "I" in str(sol)]

    else:
        for sol in solutions:
            if not False in [not "I" in str(sol.get(key)) for key in sol]:
                real_solutions.append(sol)

    if real_solutions == [] or real_solutions == {}:
        return "No solution"

    elif pprint:
        pprint_solution = ""
        for i, sol in enumerate(real_solutions):
            pprint_solution += (
                str(sol)
                .replace(":", " =")
                .replace("{", "")
                .replace("}", "")
                .replace(",", " ∧")
            )
            if i < len(real_solutions) - 1:
                pprint_solution += "    ∨    "

        return pprint_solution
    else:
        return real_solutions


def Solve(*equations, variables=None, pprint=True):
    """Alternative way to write `solve`."""
    return solve(*equations, variables=variables, pprint=pprint)


def _solve_inequality(expr, variables=None):
    import sympy

    if variables:
        solution = sympy.solve(expr, variables, dict=True)
    else:
        solution = sympy.solve(expr, dict=True)

    solution = simplify_solution(solution)

    return solution
