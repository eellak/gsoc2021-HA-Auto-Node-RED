from commlib.endpoints import endpoint_factory, EndpointType, TransportType
from commlib.transports.mqtt import ConnectionParameters, Credentials

# An index of all current Entities
class EntityIndex:
    # Array with references to all entities
    entityIndex = []

    # Add an Entity to the index
    def add_entity(self, new_entity):
        self.entityIndex.append(new_entity)


# A class representing an entity communicating via an MQTT broker on a specific topic
class Entity:
    def __init__(self, name, topic, host, username, password):
        # Entity name
        self.name = name

        # MQTT topic for Entity
        self.topic = topic

        # Entity state
        self.state = {}
        self.old_states = []

        # Automations with conditions that involve this entity
        self.automations = []

        # Add a reference of this Entity in the EntityIndex
        EntityIndex.add_entity(EntityIndex, self)

        # Create and start MQTT subscriber and related data
        self.host = host
        self.username = username
        self.password = password
        self.credentials = Credentials(username, password)
        self.conn_params = ConnectionParameters(host=host, creds=self.credentials)
        self.mqtt_sub = endpoint_factory(EndpointType.Subscriber, TransportType.MQTT)(
            topic=topic,
            conn_params=self.conn_params,
            on_message=self.update_state
        )
        self.mqtt_sub.run()

    # Adds an Automation reference to this Entity
    def add_automation(self, automation):
        self.automations.append(automation)

    # Callback function for updating Entity state and triggering automations evaluation
    def update_state(self, new_state):
        # Append old state to old states collection
        self.old_states.append(self.state)

        # Update state
        self.state = new_state

        # Iterate through automations and evaluate them
        for automation in self.automations:
            automation.evaluate()
