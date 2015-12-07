import json
from kivy.app import App


class RelayrSensorApp(App):
    def __init__(self, **kwargs):
        super(RelayrSensorApp, self).__init__(**kwargs)
        from kivy.storage.jsonstore import JsonStore
        self.relayr_config = JsonStore('relayr_credentials.json')

        self.relayr_configure()

    def mqtt_callback(self, topic, payload):
        self.root.update(topic, payload)

    def relayr_configure(self):
        from relayr import Client
        from relayr.dataconnection import MqttStream
        self.client = Client(token=self.relayr_config["token"])
        self.devices = {self.client.get_device(id=device['id']): device['name'] for device in
                        self.relayr_config["devices"]}

        self.mqtt_stream = MqttStream(self.mqtt_callback, self.devices.keys())

    def on_start(self):
        self.mqtt_stream.start()

    def on_pause(self):
        self.mqtt_stream.stop()

    def on_resume(self):
        self.mqtt_stream.start()

    def on_stop(self):
        self.mqtt_stream.stop()

    def build(self):
        from widgets import MainWidget
        return MainWidget(self.devices)


from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)

app = RelayrSensorApp()
app.run()
