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
    """
    The Entity class represents an entity communicating via an MQTT broker on a specific topic.
    ...

    Attributes
    ----------
        name: str
            Entity name. e.g: 'temperature_sensor'
        topic: str
            MQTT topic on which entity communicates. e.g: 'sensors.temp_sensor' correspons to topic sensors/temp_sensor
        host: str
            IP address of the MQTT broker used for communications. e.g: '192.168.1.2'
        username: str
            Username used for MQTT broker authentication
        password: str
            Password used for MQTT broker authentication
        state: dictionary
            Dictionary from the entity's state JSON. Initial state is a blank dictionary {}
        old_states: list
            List of dictionaries containing past states
        automations: list
            List of references to automations of which the conditions refer to this entity
        credentials: Credentials object from commlib-py
        conn_params: ConnectionParameters object from commlib-py
        mqtt_sub: MQTT subscriber object from commlib-py


    """
    def __init__(self, name, topic, host, username, password):
        """
        Creates and returns an Entity object
        :param name: Entity name. e.g: 'temperature_sensor'
        :param topic: MQTT topic on which entity communicates. e.g: 'sensors.temp_sensor' correspons to topic sensors/temp_sensor
        :param host: IP address of the MQTT broker used for communications. e.g: '192.168.1.2'
        :param username: Username used for MQTT broker authentication
        :param password: Password used for MQTT broker authentication
        """
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
        """
        Adds an Automation reference to this Entity. Meant to be called by the Automation constructor
        :param automation: Reference to the Automation object
        :return:
        """
        self.automations.append(automation)

    # Callback function for updating Entity state and triggering automations evaluation
    def update_state(self, new_state):
        """
        Function for updating Entity state and triggering automations evaluation. Meant to be used as a callback
        function by the Entity's mqtt_sub MQTT subscriber object (commlib-py).
        :param new_state: Dictionary containing the Entity's state
        :return:
        """
        # Append old state to old states collection
        self.old_states.append(self.state)

        # Update state
        self.state = new_state

        # Iterate through automations and evaluate them
        for automation in self.automations:
            automation.evaluate()
