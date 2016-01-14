# coding=utf-8

import json
import datetime
from collections import defaultdict

from kivy import Logger
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.properties import NumericProperty, DictProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.animation import Animation
try:
    # try import local graph first, if present (workaround on OS X)
    from graph import Graph, MeshLinePlot
except ImportError:
    from kivy.garden.graph import Graph, MeshLinePlot

import settings


class MainWidget(TabbedPanel):
    def __init__(self, devices, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.devices = {}
        for device, name in devices.items():
            widget = DeviceWidget()
            widget.device_id = device.id
            widget.text = name
            self.devices[device.id] = widget
            self.add_widget(widget)

    def update(self, topic, payload):
        Logger.info("main: update for %s" % topic)
        payload = json.loads(payload)
        device_id = payload['deviceId']
        readings = payload['readings']
        self.devices[device_id].update(readings)


class SensorHistoryWidget(Graph):
    meaning = StringProperty()

    def on_meaning(self, widget, meaning):
        self.ylabel = settings.UNITS.get(self.meaning, '?')
        self.ymin = settings.VALUE_BORDERS.get(self.meaning, (0, 100))[0]
        self.ymax = settings.VALUE_BORDERS.get(self.meaning, (0, 100))[1]
        self.y_ticks_major = settings.VALUE_GRAPH_TICKERS.get(self.meaning, 10)
        self.plot.color = settings.MEANING_COLORS.get(self.meaning, (.3, .3, .3, 1))
        self.update_plot()

    def __init__(self, *args, **kwargs):
        super(SensorHistoryWidget, self).__init__(*args, **kwargs)
        self.plot = MeshLinePlot()
        self.add_plot(self.plot)
        self.values = defaultdict(list)
        self.timestamps = defaultdict(list)

    def update_plot(self):
        new_points = []
        for i in xrange(len(self.timestamps[self.meaning])):
            v = self.values[self.meaning][i]
            t = self.timestamps[self.meaning][i]
            read_time = datetime.datetime.fromtimestamp(t / 1e3)
            read_ago = datetime.datetime.now() - read_time
            new_points.append((int(-read_ago.total_seconds()), v))
        self.plot.points = new_points

        if self.plot.points:
            self.xmin = self.plot.points[0][0]
            self.xmax = self.plot.points[-1][0] + 1

    def add_value(self, value, timestamp):

        self.values[self.meaning].append(value)
        self.timestamps[self.meaning].append(timestamp)
        self.update_plot()


class DeviceWidget(TabbedPanelItem):
    device_id = StringProperty("ddd")

    name_label = ObjectProperty()
    sensor_container = ObjectProperty()

    def __init__(self, **kwargs):

        super(DeviceWidget, self).__init__(**kwargs)
        self.sensors = {}
        self.history = SensorHistoryWidget()
        self.main_container.add_widget(self.history)

    def activate_history(self, meaning):
        self.history.meaning = meaning

    def on_device_id(self, device, device_id):
        self.name_label.text = device_id

    def update(self, readings):
        for reading in readings:
            meaning = reading['meaning']
            if meaning not in settings.MEANING_COLORS:
                continue
            if meaning not in self.sensors:
                sensor = SensorWidget(device=self)
                sensor.meaning = meaning
                self.sensors[meaning] = sensor
                self.sensor_container.add_widget(sensor)

                if not self.history.meaning:
                    self.history.meaning = meaning

            self.sensors[meaning].timestamp = reading['recorded']
            try:
                self.sensors[meaning].value = reading['value']
            except ValueError:
                Logger.error("Sensor: %s:%s got bad value %s" % (self.device_id, meaning, reading['value']))
                self.sensors[meaning].value = 0

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
