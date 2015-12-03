# coding=utf-8
import json
from kivy import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
import datetime
from kivy.properties import NumericProperty, DictProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.animation import Animation
from kivy.garden.graph import Graph, MeshLinePlot


class MainWidget(BoxLayout):
    def __init__(self, devices, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.devices = {}
        for device in devices:
            widget = DeviceWidget()
            widget.device_id = device.id
            self.devices[device.id] = widget
            self.add_widget(widget)

    def update(self, topic, payload):
        Logger.info("main: update for %s" % topic)
        payload = json.loads(payload)
        device_id = payload['deviceId']
        readings = payload['readings']
        self.devices[device_id].update(readings)


# graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
#               x_ticks_major=25, y_ticks_major=1,
#               y_grid_label=True, x_grid_label=True, padding=5,
#               x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1)


class SensorHistoryWidget(Graph):
    values = DictProperty()
    meaning = StringProperty()

    def __init__(self, *args, **kwargs):
        super(SensorHistoryWidget, self).__init__(*args, **kwargs)
        from math import sin
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        self.add_plot(plot)

    def add_value(self, value, timestamp):
        pass


class DeviceWidget(BoxLayout):
    device_id = StringProperty("ddd")

    name_label = ObjectProperty()
    sensor_container = ObjectProperty()

    def __init__(self, **kwargs):

        super(DeviceWidget, self).__init__(**kwargs)
        self.sensors = {}
        self.history = SensorHistoryWidget()
        self.add_widget(self.history)

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
    timestamp = NumericProperty()

    center_label = ObjectProperty()

    color = ObjectProperty([0, 0, 0, 1])

    angle = NumericProperty()

    MEANING_COLORS = {
        "temperature": get_color_from_hex("0088aaff"),
        "humidity": get_color_from_hex("00aa44ff"),
    }

    UNITS = {
        "temperature": u"°C",
        "humidity": "%",
    }

    VALUE_BORDERS = {
        "temperature": (20., 30.),
        "humidity": (0., 100.),
    }

    LABEL_PATTERN = "%s\n[b][size=20sp]%s %s[/size][/b]\n[color=918a6fff]%s sec ago[/color]"

    def update(self, sensor, value):
        read_time = datetime.datetime.fromtimestamp(self.timestamp / 1e3)

        read_ago = datetime.datetime.now() - read_time

        unit = self.UNITS.get(self.meaning, "")
        self.center_label.text = self.LABEL_PATTERN % (self.meaning, self.value, unit, int(read_ago.total_seconds()))
        self.color = self.MEANING_COLORS.get(self.meaning, (.5, 5, .5, 1))

        min_value, max_value = self.VALUE_BORDERS.get(self.meaning, (None, None))
        if min_value is None:
            self.angle = 360
        else:
            interval = max_value - min_value
            percentage = (float(self.value) - min_value) / interval
            Animation(angle=360 * percentage, d=.5, t='in_out_cubic').start(self)

    on_meaning = on_value = on_timestamp = update
