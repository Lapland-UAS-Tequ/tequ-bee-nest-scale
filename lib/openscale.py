import ujson
from utility import log
from sys import print_exception
from machine import Pin
from utime import sleep_ms
from ubinascii import unhexlify, hexlify
from machine import UART

class openScale:
    def __init__(self, txPin='P3', rxPin='P4'):
        log("openScale: Initializing...")
        self.txPin = txPin
        self.rxPin = rxPin
        self.uart = UART(1, baudrate=9600, pins=(txPin,rxPin))
        #self.timeout_chars = 50

    def readScaleValues(self):
        #Trigger reading by sending 0 (0x30) ASCII code 48
        count = 0
        data = None
        i = 0
        values = None

        while data != b'Readings:\r\n':
            data = self.uart.readline()
            #print(data)
            count = count + 1
            sleep_ms(50)

            if data != None:
                print(data)

            if count > 300:
                break

        while i<2:
            log("openScale: readScaleValues")
            self.uart.write(b'\x30')
            sleep_ms(1000)
            data = self.uart.readline()

            if data != None:
                print(data)
                values = data.decode().split(',')
                print(values)
            sleep_ms(250)
            i = i + 1


        return values

    def closeUART(self):
        log("openScale: Close UART")
        self.uart.deinit()
