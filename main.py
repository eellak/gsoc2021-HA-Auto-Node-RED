from lib.entity import Entity, EntityIndex
from lib.automation import Automation, AutomationIndex

if __name__ == '__main__':
    # MQTT Broker Config
    host = 'HOST_IP'
    username = 'BROKER_USERNAME'
    password = 'BROKER_PASSWORD'

    # Create sensor Entities
    temp_sensor = Entity(name='temperature_sensor',
                         topic='mqtt_sensors.temperature_sensor',
                         host=host,
                         username=username,
                         password=password)

    status_sensor = Entity(name='status_sensor',
                           topic='mqtt_sensors.status_sensor',
                           host=host,
                           username=username,
                           password=password)

    # Create Automation actions and conditions using closures
    def automation_action_generator(sensor):
        def automation_action():
            sensor.state = {'state': 'altered'}
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
        To test that everything works as intended just push an MQTT message to the qtt_sensors/temperature_sensor topic
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
