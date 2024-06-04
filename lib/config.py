#Configuration file
from ubinascii import unhexlify
import ujson
from sys import print_exception

class config:
    def __init__(self):
        print("initializing config...")
        #Times are set in milliseconds
        #1 min => 60000
        self.MEASUREMENT_INTERVAL = 6 * 60 * 60000
        #self.MEASUREMENT_INTERVAL = 5 * 60000

        # Send report every n boot cycle
        self.REPORT_INTERVAL = 1

        # Time in milliseconds when watchdog will timeout
        #1 min => 60000
        self.WATCHDOG_TIMEOUT_MS = 90000

        # Number of boot cycles that battery is expected to last
        self.EXPECTED_BATTERY_LIFE = 10000

        # PIN settings
        # self.DCDC_ENABLE_PIN = "P2"

        self.readConfig()

    def WATCHDOG_TIMEOUT_MS(self):
        return self.WATCHDOG_TIMEOUT_MS

    def setLORAWAN(self):
        self.LORAWAN = True
        self.SIGFOX = False
        self.WLAN = False
        self.writeConfig()

    def setSIGFOX(self):
        self.LORAWAN = False
        self.SIGFOX = True
        self.WLAN = False
        self.writeConfig()

    def setWLAN(self):
        self.LORAWAN = False
        self.SIGFOX = False
        self.WLAN = True
        self.writeConfig()

    def readConfig(self):
        try:
            config_file = open('config.json', 'r')
            config_json = ujson.loads(config_file.read())
            print(config_json)
            self.LORAWAN = config_json["LORAWAN"]
            self.SIGFOX = config_json["SIGFOX"]
            self.WLAN = config_json["WLAN"]
            self.SERVER_URL = config_json["SERVER_URL"]
            self.SSID = config_json["SSID"]
            self.PASSWORD = config_json["PASSWORD"]
            self.LORA_APP_EUI = config_json["LORA_APP_EUI"]
            self.LORA_APP_KEY = config_json["LORA_APP_KEY"]
            self.DCDC_ENABLE_PIN = config_json["DCDC_ENABLE_PIN"]
            self.TASK_DONE_PIN = config_json["TASK_DONE_PIN"]
            self.USE_NANO_TIMER = config_json["USE_NANO_TIMER"]
        except Exception as e:
            print_exception(e)
            print("Reading config...FAILED => Set defaults")
            self.LORA_APP_EUI = ''
            self.LORA_APP_KEY = ''
            self.SERVER_URL = "https://data.tequ.fi/api/beescale",
            self.SSID = ""
            self.PASSWORD = ""
            self.LORAWAN = True
            self.SIGFOX = False
            self.WLAN = False
            self.DCDC_ENABLE_PIN = "P2"
            self.TASK_DONE_PIN = "P10"
            self.USE_NANO_TIMER = False
            self.writeConfig()
        else:
            print("Reading config...OK")
        finally:
            config_file.close()

    def writeConfig(self):
        try:
            config_file = open('config.json', 'w')
            configJSON = {
                             "LORAWAN":self.LORAWAN,
                             "SIGFOX":self.SIGFOX,
                             "WLAN":self.WLAN,
                             "LORA_APP_EUI":self.LORA_APP_EUI,
                             "LORA_APP_KEY":self.LORA_APP_KEY,
                             "SERVER_URL":self.SERVER_URL,
                             "SSID":self.SSID,
                             "PASSWORD":self.PASSWORD,
                             "DCDC_ENABLE_PIN":self.DCDC_ENABLE_PIN,
                             "TASK_DONE_PIN": self.TASK_DONE_PIN,
                             "USE_NANO_TIMER": self.USE_NANO_TIMER
            }
            config_file.write(ujson.dumps(configJSON))

        except Exception as e:
            print_exception(e)
            print("Writing config...FAILED")
        else:
            print(configJSON)
            print("Writing config...OK")
        finally:
            config_file.close()

    def defaultConfig(self):
        try:
            config_file = open('config.json', 'w')

            defaultJSON = {
                             "LORAWAN":False,
                             "SIGFOX":False,
                             "WLAN":False,
                             "LORA_APP_EUI":"",
                             "LORA_APP_KEY":"",
                             "SERVER_URL": "https://data.tequ.fi/api/beescale",
                             "SSID":"eyesonhives",
                             "PASSWORD":"beewatch",
                             "DCDC_ENABLE_PIN":"P2",
                             "TASK_DONE_PIN":"P10",
                             "USE_NANO_TIMER": False,
            }

            config_file.write(ujson.dumps(defaultJSON))
        except Exception as e:
            print_exception(e)
            print("Creating default config...FAILED")
        else:
            print("Creating default config...OK")
        finally:
            config_file.close()
