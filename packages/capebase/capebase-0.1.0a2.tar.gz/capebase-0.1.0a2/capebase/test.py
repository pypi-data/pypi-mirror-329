import ast
import re
from typing import Dict

def transform_policy_expression(expr: str) -> str:
    """
    Naively convert DSL syntax to Python syntax.
    For example, replace ' = ' with ' == '.
    Adjust the regex if your DSL gets more complex.
    """
    # This regex replaces " = " with " == " when not inside quotes.
    # It is a simple approach and may need refinement for production use.
    return re.sub(r'\s=\s', ' == ', expr)

def parse_policy_expression(expr: str) -> ast.Expression:
    """
    Transform the DSL expression into a valid Python expression,
    then parse it into an AST.
    """
    transformed_expr = transform_policy_expression(expr)
    try:
        tree = ast.parse(transformed_expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Failed to parse expression '{expr}'. Transformed: '{transformed_expr}'") from e
    return tree

def parse_policy(policy: Dict[str, str]) -> Dict[str, ast.Expression]:
    """
    Given a policy dictionary (e.g. {"read": "auth.org_id = org_id", ...}),
    return a dictionary mapping each action to its parsed AST.
    """
    parsed = {}
    for action, expr in policy.items():
        parsed[action] = parse_policy_expression(expr)
    return parsed

# Example usage:
policy_definition = {
    "read": "auth.org_id = org_id",
    "create": "auth.role = 'editor'",
    "update": "(auth.id = owner_id) and (auth.org_id = org_id)",
    "delete": "auth.role = 'admin'"
}

parsed_policy = parse_policy(policy_definition)

# To see the result, you can print the AST for each policy:
for action, tree in parsed_policy.items():
    print(f"Policy for {action}:")
    print(ast.dump(tree, indent=4))
