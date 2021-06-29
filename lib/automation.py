from textx import textx_isinstance, get_metamodel

# List of primitive types that can be directly printed
primitives = (int, float, str, bool)

# Lambdas used to build expression strings based on their corresponding operators
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


# Returns printed version of operand if operand is a primitive.
# Else if attribute returns code pointing to the Attribute.
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


# A class representing an Automation
class Automation:
    """
    The Automation class represents an automation that evaluates a condition to execute an action.
    ...

    Attributes
    ----------
        name: str
            Automation name. e.g: 'open_lights'
        enabled: bool
            Whether the automation should be evaluated or not. e.g: True->Enabled, False->Disabled
        condition: function (closure)
            A condition function to be evaluated
        actions: list
            A list of Action objects to be executed
    Methods
    -------
        evaluate(self): Evaluates the Automation's conditions and runs the actions. Meant to be run by the
            update_state() function in the Entities listed in condition_entities upon them updating their states.
    """

    def __init__(self, parent, name, condition, actions, enabled):
        """
        Creates and returns an Automation object
        :param name: Automation name. e.g: 'open_lights'
        :param enabled: Whether the automation should be evaluated or not. e.g: True->Enabled, False->Disabled
        :param condition: A condition function to be evaluated
        :param actions: An action function to execute in response the successful evaluation of the condition() function
        """
        # TextX parent attribute. Required to use Automation as a custom class during metamodel instantiation
        self.parent = parent
        # Automation name
        self.name = name
        # Automation Condition
        self.condition = condition
        # Boolean variable indicating if the Automation is enabled and should be evaluated
        self.enabled = enabled
        # Action function
        self.actions = actions

    # Evaluate the Automation's conditions and run the actions
    def evaluate(self):
        """
            Evaluates the Automation's conditions if enabled is True and runs the actions.
        :return:
        """
        # Check if condition has been build using build_expression
        if self.enabled:
            if hasattr(self.condition, 'cond_lambda'):
                # Evaluate condition providing the textX model as global context for evaluation
                if eval(self.condition.cond_lambda, {'model': self.parent}):
                    self.trigger()
                    return f"{self.name}: triggered."
                else:
                    return f"{self.name}: not triggered."
            else:
                return f"{self.name}: condition not built. Please build using build_expression."
        else:
            return f"{self.name}: Automation disabled."

    # Run Automation's actions
    def trigger(self):
        # Dictionary that maps Entities to the data that should be sent to them
        messages = {}
        # Iterate over actions to form messages for each Entity
        for action in self.actions:
            # If entity of action already in messages, update the message. Else insert it.
            if action.attribute.parent in messages.keys():
                messages[action.attribute.parent].update({action.attribute.name: action.value})
            else:
                messages[action.attribute.parent] = {action.attribute.name: action.value}

        # Iterate over Entities and their corresponding messages
        for entity, message in messages.items():
            # Send message via Entity's publisher
            entity.publisher.publish(message)

    # Post-Order traversal of Condition tree, generating the condition for each node
    def process_node_condition(self, cond_node):

        # Get the full metamodel
        metamodel = get_metamodel(self.parent)

        # If we are in a ConditionGroup node, recursively visit the left and right sides
        if textx_isinstance(cond_node, metamodel.namespaces['automation']['ConditionGroup']):

            # Visit left node
            self.process_node_condition(cond_node.r1)
            # Visit right node
            self.process_node_condition(cond_node.r2)
            # Build lambda
            cond_node.cond_lambda = (operators[cond_node.operator])(cond_node.r1.cond_lambda, cond_node.r2.cond_lambda)

        # If we are in a primitive condition node, form conditions using operands
        else:
            operand1 = print_operand(cond_node.operand1)
            operand2 = print_operand(cond_node.operand2)
            cond_node.cond_lambda = (operators[cond_node.operator])(operand1, operand2)

    # Builds Automation Condition into Python expression string so that it can later be evaluated using eval()
    def build_condition(self):
        self.process_node_condition(self.condition)


class Action:
    def __init__(self, parent, attribute, value):
        self.parent = parent
        self.attribute = attribute
        self.value = value


class IntAction(Action):
    def __init__(self, parent, attribute, value):
        super(IntAction, self).__init__(parent, attribute, value)


class FloatAction(Action):
    def __init__(self, parent, attribute, value):
        super(FloatAction, self).__init__(parent, attribute, value)


class StringAction(Action):
    def __init__(self, parent, attribute, value):
        super(StringAction, self).__init__(parent, attribute, value)


class BoolAction(Action):
    def __init__(self, parent, attribute, value):
        super(BoolAction, self).__init__(parent, attribute, value)
