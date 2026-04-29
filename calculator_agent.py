import ast
import operator as _op
import re
from typing import Any

from agents import Agent, function_tool, ModelSettings

print("[calculator] 🧮 Initializing calculator agent...")

_ALLOWED_OPS = {
    ast.Add: _op.add,
    ast.Sub: _op.sub,
    ast.Mult: _op.mul,
    ast.Div: _op.truediv,
    ast.Pow: _op.pow,
    ast.USub: _op.neg,
    ast.Mod: _op.mod,
}


def _eval_ast(node: ast.AST) -> Any:
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_eval_ast(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_eval_ast(node.left), _eval_ast(node.right))
    raise ValueError("Unsupported expression")


@function_tool
def eval_expression(expression: str) -> str:
    print(f"[calculator] ➗ Evaluating: {expression}")

    expr = expression.strip().replace("^", "**")

    if not re.fullmatch(r"[\d\s\(\)\+\-\*/\.\^%]+", expr):
        print("[calculator] Invalid expression")
        return "Error: arithmetic only"

    try:
        tree = ast.parse(expr, mode="eval")
        result = str(_eval_ast(tree.body))
        print(f"[calculator]  Result: {result}")
        return result
    except Exception as e:
        print(f"[calculator]  Error: {e}")
        return f"Error: {e}"


calculator_agent = Agent(
    name="Calculator",
    instructions=(
        "You are a precise calculator. "
        "When handed arithmetic, call the eval_expression tool and return only the final numeric result."
    ),
    tools=[eval_expression],
    model_settings=ModelSettings(temperature=0),
)

print("[calculator]  Calculator agent ready")
