# boot.py -- run on boot-up
import config
config = config.config()

from machine import WDT, deepsleep, pin_sleep_wakeup
wdt = WDT(timeout=config.WATCHDOG_TIMEOUT_MS)
from utime import ticks_ms, ticks_diff, sleep_ms
start_ticks = ticks_ms
from utility import log, releasePinHold, setPinHold, changePin, setPin
from utility import blinkLED
from pycom import heartbeat
heartbeat(False)

# variables
led_time = 250
button_push_period = 0
forced_reset = False
blinkLED("blue",led_time,1)
from os import dupterm
from machine import UART, Pin
from sys import print_exception

primaryUART = UART(0, 115200)
dupterm(primaryUART)

log("Boot: Starting Bee-IoT-Scale-App-v1.0 (2022-03-14)...")

# import libaries
from machine import reset_cause, wake_reason
from utility import setToNVRAM, getFromNVRAM, getBootCountFromNVRAM, setBootCountToNVRAM
import machine

try:
    bootCount = getBootCountFromNVRAM() + 1
    reset_cause = reset_cause()
    wake_reason = wake_reason()

    log("Main: Reset cause: %s" % (reset_cause))
    log("Main: Wake up reason: %s %s" % (wake_reason[0],wake_reason[1]))

    if(reset_cause == machine.PWRON_RESET):
        log("Main: Forced system reset..(PWRON_RESET).")
        forced_reset = True
        bootCount = 1
    elif(reset_cause == machine.HARD_RESET):
        log("Main: Forced system reset (HARD_RESET)....")
        forced_reset = True
        bootCount = 1
    elif(reset_cause == machine.WDT_RESET):
        log("Main: Forced system reset (WDT_RESET)...")
        forced_reset = True
    elif(reset_cause == machine.DEEPSLEEP_RESET):
        log("Main: Deepsleep reset, this is expected behaviour")
        forced_reset = False
    elif(reset_cause == machine.SOFT_RESET):
        log("Main: SOFT Reset...")
    elif(reset_cause == machine.BROWN_OUT_RESET):
        log("Main: Brown out reset...")
        forced_reset = True

    if wake_reason[0] == machine.PWRON_WAKE:
        log("Main: Woke up by reset button")
    elif wake_reason[0] == machine.PIN_WAKE:
        log("Main: Woke up by external pin (external interrupt)")
        read_sensors = True
    elif wake_reason[0] == machine.RTC_WAKE:
        log("Main: Woke up by RTC (timer ran out)")
    elif wake_reason[0] == machine.ULP_WAKE:
        log("Main: Woke up by ULP (capacitive touch)")
except Exception as e:
    print_exception(e)

log("Main: bootCount: %d" % (bootCount))
setBootCountToNVRAM(bootCount)
sleep_time = config.MEASUREMENT_INTERVAL
