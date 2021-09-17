import time, gc, os
import neopixel
import feathers2neo
import rgb_matrix
from machine import Pin

# Create a NeoPixel instance
# Brightness of 0.3 is ample for the 1515 sized LED
pixel = neopixel.NeoPixel(Pin(feathers2neo.RGB_DATA), 1)

# Say hello
print("\nHello from FeatherS2 Neo!")
print("-------------------------\n")

# Show available memory
print("Memory Info - gc.mem_free()")
print("---------------------------")
print("{} Bytes\n".format(gc.mem_free()))

flash = os.statvfs('/')
flash_size = flash[0] * flash[2]
flash_free = flash[0] * flash[3]
# Show flash size
print("Flash - os.statvfs('/')")
print("---------------------------")
print("Size: {} Bytes\nFree: {} Bytes\n".format(flash_size, flash_free))

print("Pixel Time!\n")

# Create a colour wheel index int
color_index = 0

# Turn on the power to the NeoPixel
feathers2neo.set_pixel_power(True)

matrix_anim = rgb_matrix.matrix_animation('spiral', 6)

# Rainbow colours on the NeoPixel
while True:
    # Get the R,G,B values of the next colour
    r,g,b = feathers2neo.rgb_color_wheel( color_index )
    # Set the colour on the NeoPixel
    pixel[0] = ( r, g, b, 0.5)
    pixel.write()
    
    # Animate the RGB Matrix
    matrix_anim.animate(r, g, b)
    
    # Increase the wheel index
    color_index += 1
        
    # Sleep for 15ms so the colour cycle isn't too fast
    time.sleep(0.025)
    
