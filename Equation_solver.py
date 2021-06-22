from sympy import exp
from sympy import Symbol
from sympy import sympify
from sympy.solvers import solve
from sympy.utilities.lambdify import lambdify, implemented_function
class Equation_Solver:
    def solve(self, eq, var=None):
        rtn_str = ""
        if not var == None:
            vars = Symbol(str(var))
            solutions = solve(eq, var)
            for sol in solutions:
                rtn_str += var + " = " + str(sol) + "\n"
            return rtn_str
        else:
            try:
                expr = exp(eq)
                sym_lst = expr.free_symbols
                sym_str = ""
                for sym in sym_lst:
                    solutions = solve(eq, sym)
                    for solution in solutions:
                        rtn_str += sym.name + " = " + str(solution) + "\n"
            except:
                return None
            return rtn_str

#es = Equation_Solver()
#print(es.solve("(234265*z+4235/5325*f+2342*p)/m*64+2534/(m*p*z+72*x)/(a*b*c*d*e*f*g)"))