# FeatherS2 MicroPython Helper Library
# 2021 Seon Rozenblum - Unexpected Maker
#
# Project home:
#   https://feathers2.io
#
# 2021-Mar-21 - v0.1 - Initial implementation

# Import required libraries
from micropython import const
from machine import Pin, SPI, ADC
import machine, time

# FeatherS2 Hardware Pin Assignments

# LDO
LDO2 = const(21)

# APA102 Dotstar pins
DOTSTAR_CLK = const(45)
DOTSTAR_DATA = const(40)

# SPI
SPI_MOSI = const(35)
SPI_MISO = const(36)
SPI_CLK = const(37)

# I2C
I2C_SDA = const(38)
I2C_SCL = const(33)

# DAC
DAC1 = const(17)
DAC2 = const(18)

# LED & Ambient Light Sensor
LED = const(13)
AMB_LIGHT = const(4)

# Helper functions

# LED & Ambient Light Sensor control
def set_led(state):
    l = Pin(LED, Pin.OUT)
    l.value(state)
    
def toggle_led(state):
    l = Pin(LED, Pin.OUT)
    l.value(not l.value())
    
# Create ADC and set attenuation and resolution for 0-3.3V 
def get_amb_light(state):
    adc = ADC(Pin(AMB_LIGHT))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_9BIT)
    return adc.read()    

# LDO2 power control
# When we manually turn off the second LDO we also set the DotStar DATA and CLK pins to input to
# prevent parasitic power from lighting the LED even with the LDO off, causing current use.
# The DotStar is a beautiful LED, but parasitic power makes it a terrible choice for battery use :( 
def set_ldo2_power(state):
    """Set the power for the on-board Dostar to allow no current draw when not needed."""
    # Set the power pin to the inverse of state
    if state:
        Pin(LDO2, Pin.OUT)  # Break the PULL_HOLD on the pin
        Pin(DOTSTAR_PWR).value(True)  # Set the pin to LOW to enable the Transistor
    else:
        Pin(LDO2, Pin.OUT)  # Break the PULL_HOLD on the pin
        Pin(DOTSTAR_PWR).value(False)

    Pin(
        DOTSTAR_CLK, Pin.OUT if state else Pin.IN
    )  # If power is on, set CLK to be output, otherwise input
    Pin(
        DOTSTAR_DATA, Pin.OUT if state else Pin.IN
    )  # If power is on, set DATA to be output, otherwise input

    # A small delay to let the IO change state
    time.sleep(0.035)


# Dotstar rainbow colour wheel
def dotstar_color_wheel(wheel_pos):
    """Color wheel to allow for cycling through the rainbow of RGB colors."""
    wheel_pos = wheel_pos % 255

    if wheel_pos < 85:
        return 255 - wheel_pos * 3, 0, wheel_pos * 3
    elif wheel_pos < 170:
        wheel_pos -= 85
        return 0, wheel_pos * 3, 255 - wheel_pos * 3
    else:
        wheel_pos -= 170
        return wheel_pos * 3, 255 - wheel_pos * 3, 0


# Go into deep sleep but shut down the APA first to save power
# Use this if you want lowest deep  sleep current
def go_deepsleep(t):
    """Deep sleep helper that also powers down the on-board Dotstar."""
    set_ldo2_power(False)
    machine.deepsleep(t)
