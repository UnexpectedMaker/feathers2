# This example requires the micropython_dotstar library
# https://github.com/mattytrentini/micropython-dotstar

from machine import SoftSPI, Pin
import feathers2 as FeatherS2
from dotstar import DotStar
import time, random, micropython, gc, esp32

# Configure SPI for controlling the DotStar
# Internally we are using software SPI for this as the pins being used are not hardware SPI pins
spi = SoftSPI(sck=Pin( FeatherS2.DOTSTAR_CLK ), mosi=Pin( FeatherS2.DOTSTAR_DATA ), miso=Pin( FeatherS2.SPI_MISO) )
# Create a DotStar instance
dotstar = DotStar(spi, 1, brightness = 0.5 ) # Just one DotStar, half brightness
# Turn on the power to the DotStar
FeatherS2.set_ldo2_power( True )

# Say hello
print("\nHello from FeatherS2!")
print("----------------------\n")

# Show available memory
print("Memory Info - gc.mem_free()")
print("---------------------------")
print("{} Bytes\n".format(gc.mem_free()))

p = esp32.Partition('vfs')
flash_size = p.ioctl(4, 0) * p.ioctl(5, 0)

# Show flash size
print("Flash - esp32.Partition('vfs')")
print("------------------------------")
print("Size: {} Bytes\n".format(flash_size))

# Create a colour wheel index int
color_index = 0

print("\nDotStar time!")

# Rainbow colours on the Dotstar
while True:
    # Get the R,G,B values of the next colour
    r,g,b = FeatherS2.dotstar_color_wheel( color_index )
    # Set the colour on the dotstar
    dotstar[0] = ( r, g, b, 0.5)
    # Increase the wheel index
    color_index += 1
    # Sleep for 20ms so the colour cycle isn't too fast
    time.sleep_ms(20)
    