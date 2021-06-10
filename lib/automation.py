# An index of all current Automations
class AutomationIndex:
    # Dictionary with references to all automations
    automation_index = {}

    # Add an Entity to the index
    def add_automation(self, name, new_automation):
        if name not in self.automation_index:
            self.automation_index[name] = new_automation


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
        condition_entities: list
            A list of references to Entity objects involved in the condition function
        action: function (closure)
            An action function to execute in response the successful evaluation of the condition() function

    Methods
    -------
        evaluate(self): Evaluates the Automation's conditions and runs the actions. Meant to be run by the
            update_state() function in the Entities listed in condition_entities upon them updating their states.
    """
    def __init__(self, name, enabled, condition, condition_entities, action):
        """
        Creates and returns an Automation object
        :param name: Automation name. e.g: 'open_lights'
        :param enabled: Whether the automation should be evaluated or not. e.g: True->Enabled, False->Disabled
        :param condition: A condition function to be evaluated
        :param condition_entities: A list of references to Entity objects involved in the condition function
        :param action: An action function to execute in response the successful evaluation of the condition() function
        """
        # Automation name
        self.name = name
        # Boolean variable indicating if the Automation is enabled and should be evaluated
        self.enabled = enabled
        # Condition function
        self.condition = condition
        # Array of Entities involved in the condition
        self.condition_entities = condition_entities
        # Link Automation in the corresponding condition Entities
        for entity in condition_entities:
            entity.add_automation(self)
        # Action function
        self.action = action
        # Array of Entities involved in the action
        # self.action_entities = action_entities
        # Add Automation to AutomationIndex
        AutomationIndex.add_automation(self=AutomationIndex, name=self.name, new_automation=self)

    # Evaluate the Automation's conditions and run the actions
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
