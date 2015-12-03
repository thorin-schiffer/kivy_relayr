# coding=utf-8
import json
from kivy import Logger
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
import datetime
from kivy.properties import NumericProperty, DictProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.animation import Animation
from kivy.garden.graph import Graph, MeshLinePlot
import settings


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


class SensorHistoryWidget(Graph):
    values = DictProperty()
    timestamps = DictProperty()
    meaning = StringProperty()

    def on_meaning(self, widget, meaning):
        self.ylabel = settings.UNITS[self.meaning]
        self.ymin = settings.VALUE_BORDERS[self.meaning][0]
        self.ymax = settings.VALUE_BORDERS[self.meaning][1]
        self.y_ticks_major = settings.VALUE_GRAPH_TICKERS[self.meaning]
        self.plot.color = settings.MEANING_COLORS[self.meaning]

    def __init__(self, *args, **kwargs):
        super(SensorHistoryWidget, self).__init__(*args, **kwargs)
        self.plot = MeshLinePlot()
        self.add_plot(self.plot)

    def add_value(self, value, timestamp):

        if not self.meaning in self.values:
            self.values[self.meaning] = []

        if not self.meaning in self.timestamps:
            self.timestamps[self.meaning] = []

        self.values[self.meaning].append(value)
        self.timestamps[self.meaning].append(timestamp)

        new_points = []
        for i in xrange(len(self.timestamps[self.meaning])):
            v = self.values[self.meaning][i]
            t = self.timestamps[self.meaning][i]
            read_time = datetime.datetime.fromtimestamp(t / 1e3)
            read_ago = datetime.datetime.now() - read_time
            new_points.append((int(-read_ago.total_seconds()), v))
        self.plot.points = new_points

        self.xmin = self.plot.points[0][0]
        self.xmax = self.plot.points[-1][0] + 1


class DeviceWidget(BoxLayout):
    device_id = StringProperty("ddd")

    name_label = ObjectProperty()
    sensor_container = ObjectProperty()

    def __init__(self, **kwargs):

        super(DeviceWidget, self).__init__(**kwargs)
        self.sensors = {}
        self.history = SensorHistoryWidget()
        self.add_widget(self.history)

    def activate_history(self, meaning):
        self.history.meaning = meaning

    def on_device_id(self, device, device_id):
        self.name_label.text = device_id

    def update(self, readings):
        for reading in readings:
            meaning = reading['meaning']
            if meaning not in self.sensors:
                sensor = SensorWidget(device=self)
                sensor.meaning = meaning
                self.sensors[meaning] = sensor
                self.sensor_container.add_widget(sensor)

                if not self.history.meaning:
                    self.history.meaning = meaning

            self.sensors[meaning].timestamp = reading['recorded']
            self.sensors[meaning].value = reading['value']

            if meaning == self.history.meaning:
                self.history.add_value(reading['value'], reading['recorded'])


class SensorWidget(ButtonBehavior, BoxLayout):
    meaning = StringProperty()
    value = NumericProperty()
    timestamp = NumericProperty()

    center_label = ObjectProperty()

    color = ObjectProperty([0, 0, 0, 1])

    angle = NumericProperty()

    device = ObjectProperty()

    LABEL_PATTERN = "%s\n[b][size=20sp]%s %s[/size][/b]\n[color=918a6fff]%s sec ago[/color]"

    def on_press(self):
        self.device.activate_history(self.meaning)

    def update(self, sensor, value):
        read_time = datetime.datetime.fromtimestamp(self.timestamp / 1e3)

        read_ago = datetime.datetime.now() - read_time

        unit = settings.UNITS.get(self.meaning, "")
        self.center_label.text = self.LABEL_PATTERN % (self.meaning, self.value, unit, int(read_ago.total_seconds()))
        self.color = settings.MEANING_COLORS.get(self.meaning, (.5, 5, .5, 1))

        min_value, max_value = settings.VALUE_BORDERS.get(self.meaning, (None, None))
        if min_value is None:
            self.angle = 360
        else:
            interval = max_value - min_value
            percentage = (float(self.value) - min_value) / interval
            Animation(angle=360 * percentage, d=.5, t='in_out_cubic').start(self)

    on_meaning = on_value = on_timestamp = update
