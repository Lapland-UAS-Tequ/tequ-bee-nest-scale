from struct import pack
from ubinascii import unhexlify, hexlify
from utime import sleep_ms
from machine import deepsleep, pin_sleep_wakeup
import DCDCControl
import openscale
from utility import packFloatValue
from utility import packByteValue
from utility import packValue

#initialize data structure
sensor_values = []
weight = -99
raw = -99
t1 = -99
t2 = -99
send_failed = False

for i in range(5):
   sensor_values.append(pack("h",int(32767)))

try:
    dcdc = DCDCControl.DCDCControl(config.DCDC_ENABLE_PIN)
    dcdc.setON()
except Exception as e:
    log("Main: Switching DCDC ON...FAILED")
    print_exception(e)
else:
    log("Main: Switching DCDC ON...OK")

try:
    scale = openscale.openScale(txPin='P3', rxPin='P4')
    data = scale.readScaleValues()
    weight = float(data[1])
    raw = float(data[3])
    t1 = float(data[4])
    t2 = float(data[5])
except Exception as e:
    log("Main: Reading Scale failed...")
    print_exception(e)
finally:
    scale.closeUART()

#Close DC/DC
try:
    dcdc.setOFF()
except Exception as e:
    log("Main: Switching DCDC OFF...FAILED")
    print_exception(e)
else:
    log("Main: Switching DCDC OFF...OK")

# PROCESS SENSOR VALUES
try:
    DATAPACKET_IDENTIFIER = 21
    log("Main: | Weight: %.2f | Raw: %.2f | T1 %.2f | T2: %.2f" % (weight, raw, t1, t2))
    sensor_values[0] = packFloatValue(weight)
    sensor_values[1] = packFloatValue(raw)
    sensor_values[2] = packFloatValue(t1)
    sensor_values[3] = packFloatValue(t2)
    sensor_values[4] = packValue(bootCount)
except Exception as e:
    print_exception(e)

# PROCESS SENSOR VALUES
# Data sending
try:
    if bootCount % config.REPORT_INTERVAL == 0 or bootCount == 1:
        log("Main: Sending data started...")
        # Create datapacket #1
        payload = packByteValue(DATAPACKET_IDENTIFIER)
        for value in sensor_values:
            payload = payload + value

        if(config.LORAWAN):
            try:
                import LoRaConnection
                loracon = LoRaConnection.LoRaConnection(forced_reset, config.LORA_APP_EUI, config.LORA_APP_KEY, USE_ADR=True)
                loracon.loraSetBatteryValue(bootCount, config.EXPECTED_BATTERY_LIFE)
                # DR== => SF12....DR=5 => SF=7
                receivedData = loracon.sendLoRaData(payload, 0, True)
                if receivedData == False:
                    log("Main: LORAWAN response: %s" % receivedData)
                    log("Main: Sending LoRaWAN data...FAILED")
                    blinkLED("red",led_time,1)
                    send_failed = True
                    loracon.eraseLoraSettings()
                else:
                    log("Main: LORAWAN response: %s" % receivedData)
                    log("Main: Sending LoRaWAN data...OK")
                    blinkLED("green",led_time,1)
                    #log("Main: LORAWAN stat: %s" % loracon.stats())
            except Exception as e:
                log("Main: Exception in sending LoRaWAN data...")
                print_exception(e)
                send_failed = True
                loracon.eraseLoraSettings()
                blinkLED("red",led_time,1)
except Exception as e:
    log("Main: Data sending failed")
    print_exception(e)
else:
    log("Main: Sending data finished.")


#Close DC/DC
try:
    dcdc.setOFF()
except Exception as e:
    log("Main: Switching DCDC OFF...FAILED")
    print_exception(e)
else:
    log("Main: Switching DCDC OFF...OK")

try:
    log("Main: Feeding watchdog...")
    wdt.feed()
except Exception as e:
    log("Main: Sleep %.3f minutes..." % (sleep_time / 60000))
    print_exception(e)
finally:
    if send_failed:
        log("Main: Sending failed trying again in 1 hour...")
        sleep_ms(100)
        primaryUART.deinit()
        deepsleep(60 * 60000)
    else:
        log("Main: Sleep %.3f minutes..." % (sleep_time / 60000))
        sleep_ms(100)
        primaryUART.deinit()
        deepsleep(sleep_time)
