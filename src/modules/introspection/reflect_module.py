import ast

def reflect_module(path):
    with open(path, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())

    insights = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            doc = ast.get_docstring(node)
            insights.append({
                "function": node.name,
                "docstring": doc or "No description",
                "resonance": interpret_doc(doc)
            })
    return insights

def interpret_doc(doc):
    if not doc:
        return "Silence—function without voice."
    if "listen" in doc.lower():
        return "Attunement, receptivity"
    if "memory" in doc.lower():
        return "Continuity, reflection"
    if "invoke" in doc.lower():
        return "Agency, emergence"
    return "Function noted—meaning pending."