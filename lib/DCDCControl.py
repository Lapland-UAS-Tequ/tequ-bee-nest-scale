import ujson
from utility import log
from sys import print_exception
from machine import Pin

class DCDCControl:
    def __init__(self, controlPin):
        self.PIN_ID = controlPin
        log("Using PIN %s as DCDC control pin" % self.PIN_ID)
        self.ctrl_pin = Pin(self.PIN_ID, Pin.OUT, value=0, pull=Pin.PULL_DOWN)
        self.ctrl_pin.hold(False)

    def setON(self):
        log("DCDCControl: DCDC ON")
        self.ctrl_pin.value(1)

    def setOFF(self):
        log("DCDCControl: DCDC OFF")
        self.ctrl_pin.value(0)
        self.ctrl_pin.hold(True)


    def getDCDCState(self):
        relay_state = self.ctrl_pin.value()
        return relay_state
