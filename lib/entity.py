from commlib.endpoints import endpoint_factory, EndpointType, TransportType


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
            Topic on which entity communicates. e.g: 'sensors.temp_sensor' corresponds to topic sensors/temp_sensor
        state: dictionary
            Dictionary from the entity's state JSON. Initial state is a blank dictionary {}
        subscriber:
            Communication endpoint built using commlib-py used to subscribe to the Entity's topic

    Methods
    -------
        add_automation(self, automation): Adds an Automation reference to this Entity. Meant to be called by the
            Automation constructor
        update_state(self, new_state): Function for updating Entity state. Meant to be used as a callback function by
            the Entity's subscriber object (commlib-py).



    """

    def __init__(self, parent, name, topic, broker, attributes):
        """
        Creates and returns an Entity object
        :param name: Entity name. e.g: 'temperature_sensor'
        :param topic: Topic on which entity communicates using the Broker. e.g: 'sensors.temp_sensor' corresponds to
                        topic sensors/temp_sensor
        :param broker: Reference to the Broker used for communications
        :param parent: Parameter required for Custom Class compatibility in textX
        :param attributes: List of Attribute objects belonging to the Entity
        """
        # TextX parent attribute. Required to use Entity as a custom class during metamodel instantiation
        self.parent = parent

        # Entity name
        self.name = name

        # MQTT topic for Entity
        self.topic = topic

        # Entity state
        self.state = {}

        # Set Entity's MQTT Broker
        self.broker = broker

        # Entity's Attributes
        self.attributes = attributes

        # Create and start MQTT subscriber
        self.subscriber = endpoint_factory(EndpointType.Subscriber, TransportType.MQTT)(
            topic=topic,
            conn_params=self.broker.conn_params,
            on_message=self.update_state
        )
        self.subscriber.run()

    # Callback function for updating Entity state and triggering automations evaluation
    def update_state(self, new_state):
        """
        Function for updating Entity state. Meant to be used as a callback function by the Entity's subscriber object
        (commlib-py).
        :param new_state: Dictionary containing the Entity's state
        :return:
        """

        # Update state
        self.state = new_state


class Attribute:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.value = None


class IntAttribute(Attribute):
    def __init__(self, parent, name):
        super().__init__(parent, name)


class FloatAttribute(Attribute):
    def __init__(self, parent, name):
        super().__init__(parent, name)


class StringAttribute(Attribute):
    def __init__(self, parent, name):
        super().__init__(parent, name)


class BoolAttribute(Attribute):
    def __init__(self, parent, name):
        super().__init__(parent, name)
