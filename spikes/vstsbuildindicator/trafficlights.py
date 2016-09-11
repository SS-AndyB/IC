#!/usr/bin/env python3

class Colours(object):
    """docstring for TrafficLightColours"""

    def __init__(self, red="RED", green="GREEN", amber="AMBER"):
        self.red = red
        self.green = green
        self.amber = amber

    def RED(self):
        return self.red

    def AMBER(self):
        return self.amber

    def GREEN(self):
        return self.green
