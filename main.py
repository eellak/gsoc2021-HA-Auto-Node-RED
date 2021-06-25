import pathlib
from textx import metamodel_from_file

from lib.automation import Automation, AutomationIndex
from lib.broker import Broker, broker_index
from lib.entity import Entity, Attribute, IntAttribute, FloatAttribute, StringAttribute, BoolAttribute
from lib.build_expression import build_condition

if __name__ == '__main__':

    # Configuration files directory
    config_dir = pathlib.Path('config')

    # === Initialize Brokers ====

    # Initialize full metamodel
    metamodel = metamodel_from_file('lang/full_metamodel.tx', classes=[Entity, Attribute, IntAttribute, FloatAttribute,
                                                                       StringAttribute, BoolAttribute])

    # Initialize full model
    model = metamodel.model_from_file('config/example.full_metamodel')

    # Build conditions
    build_condition(model.automations[0].condition, metamodel)
    print(model.automations[0].condition.cond_lambda)

"""
        To test that everything works as intended just push an MQTT message to the mqtt_sensors/temperature_sensor topic
        with a temperature value > 10 and see if status_sensor's status changes to altered.
        
        Example message:
        {
          "header": {
            "timestamp": 1623231268109,
            "properties": {
              "content_type": "application/json",
              "content_encoding": "utf8"
            }
          },
          "data": {
            "temperature": 13
          }
        }
        
    """
