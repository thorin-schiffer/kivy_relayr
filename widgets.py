from boto.sdb.db.property import StringProperty
from kivy.uix.widget import Widget

from kivy.properties import NumericProperty, DictProperty


class MainWidget(Widget):
    pass


class DeviceWidget(Widget):
    def read_callback(self):
        raise NotImplementedError()


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
