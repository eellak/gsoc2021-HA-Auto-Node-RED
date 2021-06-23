from textx import textx_isinstance

# PlantUML Code
depth = 1

primitives = (int, float, str, bool)


def printOperand(node):
    if type(node) in primitives:
        return node
    else:
        return node.parent.name + '.' + node.name


# Pre-Order traversal of Condition tree
def visitNode(node, depth, metamodel, file_writer):
    # Increase depth
    depth += 1

    # Print node operator
    file_writer.write(f"{'-' * depth} {node.operator}\n")

    # If we are in a ConditionGroup node, recursively visit the left and right sides
    if textx_isinstance(node, metamodel.namespaces['automation']['ConditionGroup']):

        # Visit left node
        visitNode(node.r1, depth, metamodel, file_writer)
        # Visit right node
        visitNode(node.r2, depth, metamodel, file_writer)

    # If we are in a primitive condition node, print it out
    else:
        operand1 = printOperand(node.operand1)
        operand2 = printOperand(node.operand2)
        file_writer.write(f"{'-' * (depth + 1)} {operand1}\n")
        file_writer.write(f"{'-' * (depth + 1)} {operand2}\n")


# Visualizes Automation Conditions and Actions using PlantUML
def visualize_automation(metamodel, automation):
    with open(f'automation_{automation.name}.pu', 'w') as f:
        # Write model start
        f.write('@startmindmap\n')
        # Write center node
        f.write("+ Then\n")
        # Write actions
        for action in automation.actions:
            f.write(f"++ {printOperand(action.attribute)} = {action.value}\n")
        # Write conditions
        visitNode(automation.condition, 1, metamodel, f)
        # Write end
        f.write("@endmindmap")
        # Close file writer
        f.close()
