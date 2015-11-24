import json
from kivy import Logger
from kivy.properties import StringProperty

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from kivy.properties import NumericProperty, DictProperty


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

    def on_device_id(self, device, device_id):
        self.name_label.text = device_id

    def update(self, readings):
        pass


class SensorWidget(Widget):
    meaning = StringProperty()
    name = StringProperty()
    value = NumericProperty()
    unit_name = StringProperty()
    timestamp = NumericProperty()


class SensorHistoryWidget(Widget):
    values = DictProperty()
    meaning = StringProperty()
    name = StringProperty()
