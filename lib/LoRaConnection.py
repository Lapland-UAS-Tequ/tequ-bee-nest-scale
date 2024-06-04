"""
Class for LoRa Connection
"""
from network import LoRa
import socket
from utility import log
from utility import mapValueToRange
from utime import sleep_ms
from ubinascii import unhexlify
from binascii import hexlify

class LoRaConnection:
    def __init__(self, forced_reset, APP_EUI, APP_KEY, USE_ADR=True):
        log("LoRaConnection: Initializing...")
        self.forced_reset = forced_reset
        self.APP_EUI = unhexlify(APP_EUI)
        self.APP_KEY = unhexlify(APP_KEY)
        self.USE_ADR = USE_ADR

        if self.USE_ADR:
            log("LoRaConnection: Opening LoRaWAN connection with ADR...")
            self.lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868, adr=True, device_class=LoRa.CLASS_A, tx_retries=3)
        else:
            log("LoRaConnection: Opening LoRaWAN connection without ADR...")
            self.lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868, adr=False, device_class=LoRa.CLASS_A, tx_retries=3)

        log("LoRaConnection: DeviceEUI: %s" % hexlify(self.lora.mac()))
        self.s = None
        self.setupLoRaConnection()

    def joined(self):
        return self.lora.has_joined()

    def setupLoRaConnection(self):
        if self.forced_reset:
            log("LoRaConnection: Forced restart... erasing NVRAM...")
            self.lora.nvram_erase()
        else:
            log("LoRaConnection: Loading LoRa settings from NVRAM...")
            self.lora.nvram_restore()

        self.joinLoRaNetwork()

    def eraseLoraSettings(self):
        log("LoRaConnection: Erasing NVRAM...")
        self.lora.nvram_erase()

    def loraSetBatteryValue(self, bootCount, lifetime):
        scaleFactor = -(254.0 / lifetime)
        value = int(scaleFactor * bootCount + 254)

        if value <= 0:
            value = 1
        elif value >= 254:
            value = 254

        log("LoRaConnection: Estimated battery level: %d" % (value))
        self.lora.set_battery_level(value)

    def loraSetBattery(self,  voltage):

        # x = input value
        # a = input range min
        # b = input range max
        # c = output range min
        # d = output range max
        value = mapValueToRange(voltage, 0, 5.1, 0, 254)
        if value <= 0:
            value = 1
        elif value >= 254:
            value = 254

        log("LoRaConnection: Estimated battery level: %d" % (value))
        self.lora.set_battery_level(value)

    def stats(self):
        return self.lora.stats()


    def joinLoRaNetwork(self):
        if self.lora.has_joined():
            log('LoRaConnection: Use settings from NVRAM to join LoRa network...')
        else:
            log('LoRaConnection: No settings in NVRAM to join LoRa network...')
            self.lora.join(activation=LoRa.OTAA, auth=(self.APP_EUI,self.APP_KEY), timeout=0, dr=0)
            i=0
            while 1:
                if self.lora.has_joined():
                    log('LoRaConnection: Joined to LoRa network ..')
                    break
                elif i > 8:
                    log('LoRaConnection: Joining to LoRa network failed..')
                    break
                else:
                    i = i + 1
                    log('LoRaConnection: Not yet joined... trying again in %d milliseconds' % (5000))
                    sleep_ms(5000)

    def openSocket(self, DR, ACK):
        log("LoRaConnection: Opening LoRaWAN socket...")
        self.s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        if not self.USE_ADR:
            log("LoRaConnection: ADR is not used... SET DR=%d" % DR)
            self.s.setsockopt(socket.SOL_LORA, socket.SO_DR,DR)

        log("LoRaConnection: Confirm uplink message... ACK FLAG.. SET ACK=%s" %  ACK)
        self.s.setsockopt(socket.SOL_LORA, socket.SO_CONFIRMED, ACK)

    def closeSocket(self):
        self.s.close()

    def sendLoRaData(self, payload, DR, ACK):
        if self.lora.has_joined():
            self.openSocket(DR, ACK)
            self.s.setblocking(True)
            self.s.send(payload)
            self.s.setblocking(False)
            self.lora.nvram_save()
            data = self.s.recv(64)
            self.closeSocket()
            return data
        else:
            return False
