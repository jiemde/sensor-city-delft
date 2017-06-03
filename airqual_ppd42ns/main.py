"""
Adapted for Pycom by Rob Braggaar
Based on example by Seeedstudio

Shinyei Model PPD42NS Particle Sensor
    min: 1 um diameter particulate matter
    output unit: pcs/L or pcs/0.01cf

    wires:
    4.75 - 5.25 V INPUT :: Red wire
    GND :: Black wire
    digital input :: Yellow wire

    current draw 90 mA
    typical startup time: 1 min (resistor heats up)
"""
import time
from machine import Pin, Timer


INPUT_PIN = 'P11'
SAMPLETIME_S = 30

# setup pin
ppd_pin = Pin(INPUT_PIN, mode=Pin.IN)

# timer object for measuring low pulse duration
chrono = Timer.Chrono()

while True:
    # start time of new sampling window in seconds
    starttime = time.time()
    # ratio of LPO time over the entire sampling window
    ratio = 0
    #  Lo Pulse Occupancy Time (LPO Time) in microseconds
    low_pulse_occ = 0
    # concentration based on LPO time and characteristics graph (datasheet)
    concentration = 0

    while time.time() - starttime <= SAMPLETIME_S:  # in sampling window
        # check if pin is low, start timing
        if ppd_pin.value() == 0:
            chrono.start()  # if it is already started it will continue counting
        # get duration of low pulse and reset timer
        else:
            low_pulse_occ += chrono.read_us()
            chrono.reset()
    # ratio: integer percentage (0 - 100%)
    ratio = low_pulse_occ / (SAMPLETIME_S * 1000000.0)
    concentration = 2.1 * (ratio ** 3) - 3.8 * (ratio ** 2) + 520 * ratio + 0.62
    if concentration != 0.62:
        print("Concentration is {} pcs/0.01cf".format(concentration))
