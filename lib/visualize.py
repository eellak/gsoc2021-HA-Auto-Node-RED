from textx import textx_isinstance
from lib.automation import Dict, List

# List of primitive types that can be directly printed
primitives = (int, float, str, bool)
# Custom classes with a __repr__ function so that returning them will print them out. E.g: List class -> python list
custom_classes = (Dict, List)


def print_operand(node):
    if type(node) in primitives or type(node) in custom_classes:
        return node
    else:
        return node.parent.name + '.' + node.name


# Pre-Order traversal of Condition tree
def visit_node(node, depth, metamodel, file_writer):
    # Increase depth
    depth += 1

    # Print node operator
    file_writer.write(f"{'-' * depth} {node.operator}\n")

    # If we are in a ConditionGroup node, recursively visit the left and right sides
    if textx_isinstance(node, metamodel.namespaces['automation']['ConditionGroup']):

        # Visit left node
        visit_node(node.r1, depth, metamodel, file_writer)
        # Visit right node
        visit_node(node.r2, depth, metamodel, file_writer)

    # If we are in a primitive condition node, print it out
    else:
        operand1 = print_operand(node.operand1)
        operand2 = print_operand(node.operand2)
        file_writer.write(f"{'-' * (depth + 1)} {operand1}\n")
        file_writer.write(f"{'-' * (depth + 1)} {operand2}\n")


# Visualizes Automation Conditions and Actions using PlantUML
def visualize_automation(metamodel, automation):
    # Initial MindMap depth
    depth = 1

    # Open output file and write
    with open(f'automation_{automation.name}.pu', 'w') as f:
        # Write MindMap model start
        f.write('@startmindmap\n')
        # Write center node
        f.write("+ Then\n")
        # Write Actions
        for action in automation.actions:
            f.write(f"++ {print_operand(action.attribute)} = {action.value}\n")
        # Write Conditions
        visit_node(automation.condition, depth, metamodel, f)
        # Write MindMap model end
        f.write("@endmindmap")
        # Close file writer
        f.close()
