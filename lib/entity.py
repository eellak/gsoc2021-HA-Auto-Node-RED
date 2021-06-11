from commlib.endpoints import endpoint_factory, EndpointType, TransportType
from commlib.transports.mqtt import ConnectionParameters, Credentials

from lib.broker import broker_index

# An index of all current Entities {'entity_name': entity_object}. Gets populated by Entity's __init()__.
entity_index = {}


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

    Methods
    -------
        add_automation(self, automation): Adds an Automation reference to this Entity. Meant to be called by the
            Automation constructor
        update_state(self, new_state): Function for updating Entity state and triggering automations evaluation. Meant
            to be used as a callback function by the Entity's mqtt_sub MQTT subscriber object (commlib-py).



    """
    def __init__(self, parent, name, topic, broker_name):
        """
        Creates and returns an Entity object
        :param name: Entity name. e.g: 'temperature_sensor'
        :param topic: MQTT topic on which entity communicates. e.g: 'sensors.temp_sensor' corresponds to topic
            sensors/temp_sensor
        :param broker_name: Name of the MQTT broker used for communications.
        :param parent: Parameter required for Custom Class compatibility in textX
        """
        # TextX parent attribute. Required to use Entity as a custom class during metamodel instantiation
        self.parent = parent

        # Entity name
        self.name = name

        # MQTT topic for Entity
        self.topic = topic

        # Entity state
        self.state = {}
        self.old_states = []

        # Automations with conditions that involve this entity
        self.automations = []

        # Add a reference of this Entity in the entity_index
        if self.name not in entity_index:
            entity_index[self.name] = self

        # Set Entity's MQTT Broker
        self.broker_name = broker_name
        self.broker = broker_index[broker_name]

        # Create and start MQTT subscriber
        self.mqtt_sub = endpoint_factory(EndpointType.Subscriber, TransportType.MQTT)(
            topic=topic,
            conn_params=self.broker.conn_params,
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
