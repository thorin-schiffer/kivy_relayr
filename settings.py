# coding=utf-8
from kivy.utils import get_color_from_hex

# coding=utf-8
MEANING_COLORS = {
    "temperature": get_color_from_hex("0088aaff"),
    "humidity": get_color_from_hex("00aa44ff"),
    "luminosity": get_color_from_hex("ffd42aff"),
    "proximity": get_color_from_hex("ff8080ff"),
    "noiseLevel": get_color_from_hex("808080ff"),
}

UNITS = {
    "temperature": u"°C",
    "humidity": "%",
    "luminosity": "%",
    "proximity": "%",
    "noiseLevel": "dB",
}

VALUE_BORDERS = {
    "temperature": (20., 30.),
    "humidity": (0., 100.),
    "luminosity": (0., 100.),
    "proximity": (0., 100.),
    "noiseLevel": (50., 150.),
}

VALUE_GRAPH_TICKERS = {
    "temperature": 2,
    "humidity": 20,
    "luminosity": 20,
    "proximity": 20,
    "noiseLevel": 20,
}
