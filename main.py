import pathlib
import time

from textx import metamodel_from_file

from lib.automation import Automation, Action, IntAction, FloatAction, StringAction, BoolAction
from lib.broker import Broker, MQTTBroker, AMQPBroker, RedisBroker, BrokerAuthPlain
from lib.entity import Entity, Attribute, IntAttribute, FloatAttribute, StringAttribute, BoolAttribute
from lib.build_expression import build_condition


# Used to initialize entities with data for condition testing purposes
def seed(entities_dict):
    # Set temperature
    entities_dict['temperature_sensor'].publisher.publish({"temperature": 8})

    # Set status
    entities_dict['status_sensor_2'].publisher.publish({"status": 'At Home'})

    # Set thermostat status
    entities_dict['thermostat'].publisher.publish({"on": False})


if __name__ == '__main__':

    # Configuration files directory
    config_dir = pathlib.Path('config')

    # === Initialize Brokers ====

    # Initialize full metamodel
    metamodel = metamodel_from_file('lang/full_metamodel.tx', classes=[Entity, Attribute, IntAttribute, FloatAttribute,
                                                                       StringAttribute, BoolAttribute, Broker,
                                                                       MQTTBroker, AMQPBroker, RedisBroker,
                                                                       BrokerAuthPlain, Automation, Action, IntAction,
                                                                       FloatAction, StringAction, BoolAction])

    # Initialize full model
    model = metamodel.model_from_file('config/example.full_metamodel')

    # Build entities dictionary in model. Needed for evaluating conditions
    model.entities_dict = {entity.name: entity for entity in model.entities}

    # Build Conditions for all Automations
    for automation in model.automations:
        build_condition(automation.condition, metamodel)
        print(f"{automation.name} condition:\n{model.automations[0].condition.cond_lambda}\n")

    # Seed the entities with initial data so the Automation will evaluate to True
    seed(model.entities_dict)

    # Evaluation loop
    counter = 1
    while counter < 24:
        # Every 4 iterations use seed to set the Automation Entities states so that the Action triggers
        if counter % 4 == 0:
            seed(model.entities_dict)
        # Evaluate automations and print results
        for automation in model.automations:
            print(automation.evaluate())
        # Increase counter
        counter += 1
        # Sleep
        time.sleep(2)
