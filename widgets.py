import json
from kivy import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex

from kivy.properties import NumericProperty, DictProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty


class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.devices = {}

    def add_device_widget(self, device_id, data):
        device = DeviceWidget()
        device.device_id = device_id
        self.devices[device_id] = device
        self.add_widget(device)

    def update(self, topic, payload):
        Logger.info("main: update for %s" % topic)

        if not self.devices:
            self.clear_widgets()

        payload = json.loads(payload)
        device_id = payload['deviceId']
        readings = payload['readings']
        if device_id not in self.devices:
            self.add_device_widget(device_id, readings)
        self.devices[device_id].update(readings)


class DeviceWidget(BoxLayout):
    device_id = StringProperty("ddd")

    name_label = ObjectProperty()
    sensor_container = ObjectProperty()

    def __init__(self, **kwargs):

        super(DeviceWidget, self).__init__(**kwargs)
        self.sensors = {}

    def on_device_id(self, device, device_id):
        self.name_label.text = device_id

    def update(self, readings):
        for reading in readings:
            meaning = reading['meaning']
            if meaning not in self.sensors:
                sensor = SensorWidget()
                sensor.meaning = meaning
                self.sensors[meaning] = sensor
                self.sensor_container.add_widget(sensor)
            self.sensors[meaning].timestamp = reading['recorded']
            self.sensors[meaning].value = reading['value']


class SensorWidget(BoxLayout):
    meaning = StringProperty()
    value = NumericProperty()
    unit_name = StringProperty()
    timestamp = NumericProperty()

    meaning_label = ObjectProperty()
    value_label = ObjectProperty()
    last_update_label = ObjectProperty()

    color = ObjectProperty([0, 0, 0, 1])

    MEANING_COLORS = {
        "temperature": get_color_from_hex("0088aaff"),
        "humidity": get_color_from_hex("00aa44ff"),
    }

    def on_meaning(self, sensor, meaning):
        self.meaning_label.text = meaning
        self.color = self.MEANING_COLORS.get(meaning, (.5, 5, .5, 1))

    def on_value(self, sensor, value):
        self.value_label.text = unicode(value)

    def on_timestamp(self, sensor, timestamp):
        self.last_update_label.text = unicode(timestamp)


class SensorHistoryWidget(Widget):
    values = DictProperty()
    meaning = StringProperty()
