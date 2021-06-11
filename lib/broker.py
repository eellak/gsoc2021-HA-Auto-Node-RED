from commlib.transports.mqtt import ConnectionParameters, Credentials

# An index of all current MQTT Brokers {'broker_name': broker_object}. Gets populated by Broker's __init()__.
broker_index = {}


# A class representing an Automation
class Broker:
    """
    The Broker class represents an MQTT broker structure used by Entities.
    ...

    Attributes
    ----------
        name: str
            Broker name. e.g: 'home_mqtt'
        host: str
            IP address of the MQTT broker used for communications. e.g: '192.168.1.2'
        username: str
            Username used for MQTT broker authentication
        password: str
            Password used for MQTT broker authentication

    Methods
    -------
    ---
    """

    def __init__(self, parent, name, host, username, password, port=1883):
        """
        Creates and returns a Broker object
        :param name: Broker name. e.g: 'home_mqtt'
        :param host: IP address of the MQTT broker used for communications. e.g: '192.168.1.2'
        :param port: Port used for MQTT broker communication
        :param username: Username used for MQTT broker authentication
        :param password: Password used for MQTT broker authentication
        :param parent: Parameter required for Custom Class compatibility in textX
        """
        # TextX parent attribute. Required to use as custom class during metamodel instantiation
        self.parent = parent
        # MQTT Broker
        self.name = name
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        # Create commlib-py Credentials and ConnectionParameters objects
        self.credentials = Credentials(username, password)
        self.conn_params = ConnectionParameters(host=host, port=port, creds=self.credentials)

        # Add Broker to broker_index
        if self.name not in broker_index:
            broker_index[self.name] = self
