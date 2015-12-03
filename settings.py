# coding=utf-8
from kivy.utils import get_color_from_hex

# coding=utf-8
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

VALUE_GRAPH_TICKERS = {
    "temperature": 2,
    "humidity": 20,
}
