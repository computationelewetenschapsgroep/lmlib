
class PreconditionNode:
    def __init__(self):
        self.value = None
        self.children = []


class PDDLPreconditionSyntaxTree:
    def __init__(self):
        self.root = PreconditionNode()
        self.leaf = root

    def add_condition(self, condition: str):
        new_node = PreconditionNode()
        new_node.value = condition
        self.root.children.append(new_node)
    
    def add_operator(self, operator: str):
        new_node = PreconditionNode()
        new_node.value = operator
        self.root.children.append(new_node)
        self.root = new_node

    def to_pddl_precondition(self) -> str:
        if not self.root.children:
            return "value"
        
        op = self.root.value
        nested_conditions = []
        for child in self.root.children:
            nested_conditions.append(child.value)
        
        precondition = PDDLPrecondition()

        return precondition  

"""
    if op in {"and", "or", "imply"}:
        return f"({op} {' '.join(nested_conditions)})"
    elif op == "not":
        return f"(not {nested_conditions[0]})"
    elif op in {"forall", "exists"}:
        var_str = " ".join(f"{v} - {t}" for v, t in nested_conditions[0])
        return f"({op} ({var_str}) {nested_conditions[1]})"
"""