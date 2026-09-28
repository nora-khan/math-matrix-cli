#!/usr/bin/env python3
"""
term-calculator — Safe expression evaluator and financial calculator.
"""
import ast
import math
import operator
import sys

ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}

ALLOWED_NAMES = {
    "pi": math.pi,
    "e": math.e,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "log": math.log,
}

def safe_eval(node):
    if isinstance(node, ast.Expression):
        return safe_eval(node.body)
    elif isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        return ALLOWED_OPS[op_type](safe_eval(node.left), safe_eval(node.right))
    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return ALLOWED_OPS[op_type](safe_eval(node.operand))
    elif isinstance(node, ast.Name):
        if node.id in ALLOWED_NAMES:
            return ALLOWED_NAMES[node.id]
        raise ValueError(f"Unknown variable: {node.id}")
    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in ALLOWED_NAMES:
            func = ALLOWED_NAMES[node.func.id]
            args = [safe_eval(arg) for arg in node.args]
            return func(*args)
        raise ValueError("Unsupported function call")
    raise TypeError(f"Unsupported AST node: {type(node).__name__}")

def evaluate_expression(expr: str):
    parsed = ast.parse(expr, mode='eval')
    return safe_eval(parsed)

def compound_interest(principal: float, rate_annual: float, years: int, times_compounded: int = 12) -> float:
    r = rate_annual / 100.0
    return principal * (1 + r / times_compounded) ** (times_compounded * years)

def main():
    if len(sys.argv) > 1:
        expr = " ".join(sys.argv[1:])
        try:
            res = evaluate_expression(expr)
            print(f"> {expr} = {res}")
        except Exception as e:
            print(f"Error: {e}")
        return

    print("=" * 50)
    print("  Terminal Scientific Calculator (AST-Safe)")
    print("=" * 50)
    print("Type expressions (e.g. 2**8 + sqrt(144)) or 'compound' for financial:")
    print("Type 'exit' to quit.
")

    while True:
        try:
            line = input("calc> ").strip()
            if not line:
                continue
            if line.lower() in ("exit", "quit", "q"):
                break
            if line.lower() == "compound":
                p = float(input("  Principal ($): "))
                r = float(input("  Annual Rate (%): "))
                y = int(input("  Duration (Years): "))
                tot = compound_interest(p, r, y)
                print(f"  Final Amount: ${tot:,.2f} (Interest: ${tot-p:,.2f})
")
                continue
            ans = evaluate_expression(line)
            print(f"  = {ans}
")
        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            print(f"  Error: {e}
")

if __name__ == "__main__":
    main()
