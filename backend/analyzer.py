import ast

def analyze_code_structure(code):

    result = {
        "lines": 0,
        "variables": 0,
        "functions": 0,
        "loops": 0,
        "ifs": 0,
        "prints": 0,
        "imports": 0
    }

    try:

        tree = ast.parse(code)

        result["lines"] = len(code.splitlines())

        for node in ast.walk(tree):

            if isinstance(node, ast.Assign):
                result["variables"] += 1

            elif isinstance(node, ast.FunctionDef):
                result["functions"] += 1

            elif isinstance(node, (ast.For, ast.While)):
                result["loops"] += 1

            elif isinstance(node, ast.If):
                result["ifs"] += 1

            elif isinstance(node, ast.Import):
                result["imports"] += 1

            elif isinstance(node, ast.ImportFrom):
                result["imports"] += 1

            elif isinstance(node, ast.Call):

                if isinstance(node.func, ast.Name):

                    if node.func.id == "print":
                        result["prints"] += 1

    except Exception:
        pass

    return result