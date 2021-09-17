# FeatherS2 Neo RGB Maxtrix Animation Library
# 2021 Seon Rozenblum, Unexpected Maker
#
# Project home:
#   https://unexpectedmaker.com/feathers2-neo
#

# Import required libraries
import time
import neopixel
import feathers2neo
from machine import Pin

class matrix_animation:
    
    def __init__(self, anim_type, trail_length, brightness = 0.3):
        
        # List of animation shapes by pixel index
        # Pixel 0 is Top Left, pixels increase vertically by row
        # Feel free to make your own shapes!   
        self.matrix_display_shapes = {
            "square": [0,1,2,3,4,9,14,19,24,23,22,21,20,15,10,5],
            "circle": [1,2,3,9,14,19,23,22,21,15,10,5],
            "diamond": [2,8,14,18,22,16,10,6],
            "plus": [2,7,12,17,22,10,11,12,13,14],
            "cross": [0,6,12,18,24,4,8,12,16,20],
            "spiral": [12,13,18,17,16,11,6,7,8,9,14,19,24,23,22,21,20,15,10,5,0,1,2,3,4,9,14,19,24,23,22,21,20,15,10,5,6,7,8,13,18,17,16,11,12,-1,-1,-1,-1,-1,-1,-1]
        }
            
        # Initialisation error status
        self.error = False
        
        if anim_type not in self.matrix_display_shapes:
            print(f"** '{anim_type}' not found in list of shapes!\n** Animation halted!")
            self.error = True
        elif trail_length < 1 or trail_length > 20:
            print(f"** trail_length cannot be {trail_length}. Please pick a value between 1 and 20!\n** Animation halted!")
            self.error = True
        
        if not self.error: 
            # Create the neopixel matrix reference
            self.matrix = neopixel.NeoPixel(Pin(feathers2neo.RGB_MATRIX_DATA), 25)
            self.anim_type = anim_type
            self.trail_length = trail_length + 1
            self.brightness = brightness
            
            # Create the trail list base don the length of the trail
            self.anim_trail = [x for x in range(0, -self.trail_length,-1)]
            
            # Create a reference to the selected animation list
            self.current_anim = self.matrix_display_shapes[self.anim_type]
            
            # Turn on the LDO that powers the RGB Matrix
            feathers2neo.set_pixel_matrix_power(True)

    def get_alpha(self):
        return 0.2 * (self.trail_length-1)
    
    def inc_anim_index(self, index):
        self.anim_trail[index] += 1
        if self.anim_trail[index] == len(self.current_anim):
            self.anim_trail[index] = 0
    
    def get_anim_index(self, index ):
        return self.current_anim[self.anim_trail[index]]
    
    def animate(self, r, g, b):
        if self.error:   
            return  
                
        alpha = self.get_alpha()
        for index in range(self.trail_length):
            if self.anim_trail[index] > -1:
                (r2, g2, b2) = int(r * alpha * self.brightness), int(g * alpha * self.brightness), int(b * alpha * self.brightness)
                if self.get_anim_index(index) > -1:
                    self.matrix[ self.get_anim_index(index) ] = (r2, g2, b2)
                alpha = alpha - 0.2 if alpha > 0.2 else 0
            
            self.matrix.write()
            self.inc_anim_index(index)
    