import os
import time
import logging
from colorama import init, Fore, Style

from textx import metamodel_from_file

from commlib.endpoints import endpoint_factory, EndpointType, TransportType
from commlib.transports.mqtt import ConnectionParameters as MQTT_ConnectionParameters, Credentials as MQTT_Credentials

from lib.automation import Automation, List, Dict, Action, IntAction, FloatAction, StringAction, BoolAction
from lib.broker import Broker, MQTTBroker, AMQPBroker, RedisBroker, BrokerAuthPlain
from lib.entity import Entity, Attribute, \
    IntAttribute, FloatAttribute, StringAttribute, BoolAttribute, ListAttribute, DictAttribute


# === Node-RED integration settings ===
# A Run Mode flag. Set to "MQTT" for the Node-RED integration, or to "Local" for a local config
RUN_MODE = "MQTT"

# Import the configuration for the broker used to receive the HA-Auto configuration model
if RUN_MODE != "Local":
    from config.config import nr_mqtt as nr


# Function used as a callback by the commlib subscriber when receiving the HA-Auto configuration from a broker.
# It extracts the configuration and writes it to a file.
def rn_start_scheduler(data):
    logging.info("Configuration Received")
    with open(f"config/config_remote.model", 'w') as f:
        f.write(data["config"])
        f.close()


if __name__ == '__main__':

    # Initialize full metamodel
    metamodel = metamodel_from_file('lang/full_metamodel.tx', classes=[Entity, Attribute, IntAttribute, FloatAttribute,
                                                                       StringAttribute, BoolAttribute, ListAttribute,
                                                                       DictAttribute, Broker, MQTTBroker, AMQPBroker,
                                                                       RedisBroker, BrokerAuthPlain, Automation, Action,
                                                                       IntAction, FloatAction, StringAction, BoolAction,
                                                                       List, Dict])

    # Determine the configuration file path: remote or local
    if RUN_MODE == "MQTT":
        # Create and run subscriber to connect to MQTT broker to receive the model sent by the Node-RED integration
        nr_credentials = MQTT_Credentials(nr["username"], nr["password"])
        nr_conn_params = MQTT_ConnectionParameters(host=nr["host"], port=nr["port"], creds=nr_credentials)
        subscriber = endpoint_factory(EndpointType.Subscriber, TransportType.MQTT)(
            topic=nr["topic"],
            conn_params=nr_conn_params,
            on_message=rn_start_scheduler
        )
        subscriber.run()

        # Wait to receive the model
        while not os.path.exists("config/config_remote.model"):
            time.sleep(1)

        # Stop the subscriber
        subscriber.stop()

        # The path where the subscriber callback saved the received model
        model_path = "config/config_remote.model"

    else:
        # Define the default local configuration path
        model_path = "config/config_local.model"

    # Parse model
    model = metamodel.model_from_file(model_path)

    # Build entities dictionary in model. Needed for evaluating conditions
    model.entities_dict = {entity.name: entity for entity in model.entities}

    # Build Conditions for all Automations
    for automation in model.automations:
        automation.build_condition()
        print(f"{automation.name} condition:\n{automation.condition.cond_lambda}\n")

    # Evaluation loop
    while True:
        # Evaluate automations, run applicable actions and print results
        for automation in model.automations:
            # Evaluate
            triggered, msg = automation.evaluate()
            # Check if action is triggered
            if triggered:
                print(f"{Fore.MAGENTA}{automation.name}: {triggered}{Style.RESET_ALL}")
                # If automation triggered run its actions
                automation.trigger()
            else:
                print(f"{automation.name}: {triggered}")

        # Sleep
        time.sleep(1)
