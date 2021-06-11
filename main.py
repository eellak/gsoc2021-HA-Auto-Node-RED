import pathlib
from textx import metamodel_from_file

from lib.automation import Automation, AutomationIndex
from lib.broker import Broker, broker_index
from lib.entity import Entity, EntityIndex
import config.config as cfg

if __name__ == '__main__':

    # Configuration files directory
    config_dir = pathlib.Path('config')

    # Initialize broker metamodel
    brokers_meta_tx = metamodel_from_file('lang/broker.tx', classes=[Broker])

    # Read Brokers from files
    brokers_files = list(config_dir.glob('*.broker'))
    brokers_files.remove(pathlib.Path("config\\broker_example.broker"))

    # Iterate through broker files and brokers. Brokers are added to the broker_index through the Broker __init()__.
    # debug_broker_index will end up being a copy of broker_index from lib.broker
    debug_broker_index = {}
    for file in brokers_files:
        for broker in brokers_meta_tx.model_from_file(file).brokers:
            debug_broker_index[broker.name] = broker

    # Create sensor Entities
    temp_sensor = Entity(name='temperature_sensor',
                         topic='mqtt_sensors.temperature_sensor',
                         broker_name='home_broker')

    status_sensor = Entity(name='status_sensor',
                           topic='mqtt_sensors.status_sensor',
                           broker_name='home_broker')

    # Create Automation actions and conditions using closures
    def automation_action_generator(sensor):
        counter = 0

        def automation_action():
            nonlocal counter
            sensor.update_state({'state': f'altered{counter}'})
            counter = counter + 1

        return automation_action


    def automation_condition_generator(sensor):

        def automation_condition():
            return sensor.state['temperature'] > 10

        return automation_condition


    # Create Automation
    automation = Automation(name='automation',
                            enabled=True,
                            condition=automation_condition_generator(temp_sensor),
                            condition_entities=[temp_sensor],
                            action=automation_action_generator(status_sensor))

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
