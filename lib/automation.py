# An index of all current Automations
class AutomationIndex:
    # Array with references to all entities
    automation_index = []

    # Add an Entity to the index
    def add_automation(self, new_automation):
        self.automation_index.append(new_automation)


# A class representing an Automation
class Automation:
    def __init__(self, name, enabled, condition, condition_entities, action):
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
        AutomationIndex.add_automation(AutomationIndex, self)

    # Evaluate the Automation's conditions and run the actions
    def evaluate(self):
        if self.enabled:
            if self.condition():
                return self.action()
            else:
                return 'Condition Failed'
        else:
            return 'Automation Disabled'
