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
    #TODO: Update this function to work with eval() and new condition builder
    def evaluate(self):
        """
            Evaluates the Automation's conditions in the enabled is True and runs the actions. Meant to be run by the
            update_state() function in the Entities listed in condition_entities upon them updating their states.
        :return:
        """
        if self.enabled:
            if self.condition():
                return self.action()
            else:
                return 'Condition Failed'
        else:
            return 'Automation Disabled'

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
