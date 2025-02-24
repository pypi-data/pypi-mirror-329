import json
from decimal import Decimal

RESERVED_WORDS = frozenset(
    """
break case catch class const continue debugger default delete do else export
extends false finally for function if import in instanceof new null return
super switch this throw true try typeof var void while with yield
""".strip().split()
)


def convert(name):
    if isinstance(name, int):
        return f"[{name}]"
    elif "-" in name or " " in name or "." in name or name in RESERVED_WORDS:
        return f"[{json.dumps(name, ensure_ascii=False)}]"
    return f".{name}"


def gron(node, name):
    if node is None:
        return f"{name} = null;"
    elif isinstance(node, dict):
        res = [f"{name} = {{}};"]
        for key, value in sorted(node.items()):
            res.append(gron(value, name + convert(key)))
        return "\n".join(sorted(res))
    elif isinstance(node, (list, tuple)):
        res = []
        res.append(f"{name} = [];")
        for index, element in enumerate(node):
            res.append(gron(element, name + convert(index)))
        return "\n".join(res)
    elif isinstance(node, bool):
        return f"{name} = {str(node).lower()};"
    elif isinstance(node, bytes):
        return f'{name} = "{node!r}";'
    elif isinstance(node, str):
        return f"{name} = {json.dumps(node, ensure_ascii=False)};"
    elif isinstance(node, Decimal):
        return f"{name} = {str(node)};"
    else:
        return f"{name} = {node!r};"
