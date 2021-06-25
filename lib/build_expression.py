from textx import textx_isinstance

# List of primitive types that can be directly printed
primitives = (int, float, str, bool)

operators = {
    # String operators
    '~': lambda left, right: f"({left} in {right})",
    '!~': lambda left, right: f"({left} not in {right})",

    # Shared operators
    '==': lambda left, right: f"({left} == {right})",
    '!=': lambda left, right: f"({left} != {right})",

    # Numeric operators
    '>': lambda left, right: f"({left} > {right})",
    '<': lambda left, right: f"({left} < {right})",

    # Boolean operators
    'AND': lambda left, right: f"({left} and {right})",
    'OR': lambda left, right: f"({left} or {right})",
    'NOT': lambda left, right: f"({left} is not {right})",
    'XOR': lambda left, right: f"({left} ^ {right})",
    'NOR': lambda left, right: f"(not ({left} or {right}))",
    'XNOR': lambda left, right: f"(({left} or {right}) and (not {left} or not {right}))",
    'NAND': lambda left, right: f"(not ({left} and {right}))"
}


def print_operand(node):
    # If node is a primitive type return as is (if string, add quotation marks)
    if type(node) in primitives:
        if type(node) is str:
            return f"'{node}'"
        else:
            return node
    # Node is an Attribute, print its full name including Entity
    else:
        return f"model.entities_dict['{node.parent.name}'].attributes_dict['{node.name}'].value"


# Post-Order traversal of Condition tree
# Builds Automation Condition into Python expression string so that it can later be evaluated using eval()
def build_condition(cond_node, metamodel):

    # If we are in a ConditionGroup node, recursively visit the left and right sides
    if textx_isinstance(cond_node, metamodel.namespaces['automation']['ConditionGroup']):

        # Visit left node
        build_condition(cond_node.r1, metamodel)
        # Visit right node
        build_condition(cond_node.r2, metamodel)
        # Build lambda
        cond_node.cond_lambda = (operators[cond_node.operator])(cond_node.r1.cond_lambda, cond_node.r2.cond_lambda)

    # If we are in a primitive condition node, form conditions using operands
    else:
        operand1 = print_operand(cond_node.operand1)
        operand2 = print_operand(cond_node.operand2)
        cond_node.cond_lambda = (operators[cond_node.operator])(operand1, operand2)
