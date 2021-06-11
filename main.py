from lib.automation import Automation, AutomationIndex
from lib.broker import Broker, BrokerIndex
from lib.entity import Entity, EntityIndex
import config as cfg

if __name__ == '__main__':

    # Create MQTT Broker object
    home_broker = Broker(name='home_broker',
                         host=cfg.mqtt["host"],
                         username=cfg.mqtt["username"],
                         password=cfg.mqtt["password"])

    # Create sensor Entities
    temp_sensor = Entity(name='temperature_sensor',
                         topic='mqtt_sensors.temperature_sensor',
                         broker=home_broker)

    status_sensor = Entity(name='status_sensor',
                           topic='mqtt_sensors.status_sensor',
                           broker=home_broker)

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
