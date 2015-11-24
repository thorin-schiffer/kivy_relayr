import json
from kivy.app import App


class RelayrSensorApp(App):
    def __init__(self, **kwargs):
        super(RelayrSensorApp, self).__init__(**kwargs)

        with open("relayr_credentials.json", "r") as f:
            self.relayr_config = json.load(f)
        self.relayr_configure()

    def mqtt_callback(self, topic, payload):
        self.root.update(topic, payload)

    def relayr_configure(self):
        from relayr import Client
        from relayr.dataconnection import MqttStream
        self.client = Client(token=self.relayr_config["token"])
        self.device = self.client.get_device(id=self.relayr_config["devices"][0]["id"])
        self.mqtt_stream = MqttStream(self.mqtt_callback, [self.device])

    def on_start(self):
        self.mqtt_stream.start()

    def on_stop(self):
        self.mqtt_stream.stop()

    def build(self):
        from widgets import MainWidget
        return MainWidget()


from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)

app = RelayrSensorApp()
app.run()
