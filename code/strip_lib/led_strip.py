import time
import board
import neopixel
from random import randint

## Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
ORANGE = (240, 128, 8)
OFF = (0, 0, 0)
WHITE = (255, 255, 255)

## LED Management Functions
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b)

def close_strip(strip):
    strip.deinit()

def clear(strip):
    strip.fill(OFF)

def clear_show(strip):
    clear(strip)
    strip.show()

def dim(color, percent):
    red, green, blue = color
    dec = percent / 100
    red = int(red * dec)
    green = int(green * dec)
    blue = int(blue * dec)
    return (red, green, blue)

def rand_color():
    return(randint(1, 255), randint(1, 255), randint(1, 255))

def rand_color_dim():
    return dim(rand_color(), randint(1, 100))

## LED Base Color Functions
def random_fill(strip):
    for x in range(len(strip)):
        strip[x] = rand_color()
    strip.show()

def random_fill_dim(strip):
    for x in range(len(strip)):
        strip[x] = rand_color_dim()
    strip.show()

def random_pixels(strip, color, number):
    for x in range(number):
        strip[randint(0, len(strip) - 1)] = color
    strip.show()

def pixel_pulse(strip, led_num, iterations = 1, wait = 0.01):
    led_color = strip[led_num]
    for i in range(iterations):
        for x in range(100):
            strip[led_num] = dim(led_color, 100 - x)
            strip.show()
            time.sleep(0.01)
        for x in range(100):
            strip[led_num] = dim(led_color, x)
            strip.show()
            time.sleep(0.01)

def pulse(strip, iterations = 1, wait = 0.01): #TODO - Test Me
    length = len(strip)
    led_values = [] # Store the current LED colors so that you can return back to them.
    for n in range(length):
        led_values.append(strip[n])

    for z in range(iterations):
        for x in range(10, 100):
            for i in range(length):
                red, green, blue = led_values[i]
                strip[i] = (int(red / (x / 10)), int(green / (x / 10)), int(blue / (x / 10)))
            strip.show()
            time.sleep(0.01)

        for x in range(10, 100):
            for i in range(length):
                red, green, blue = led_values[i]
                strip[i] = (int(red / ((110 - x) / 10)), int(green / ((110 - x) / 10)), int(blue / ((110 - x) / 10)))
            strip.show()
            time.sleep(0.01)

def alternate(strip, color1, color2, iterations = 2, wait = 0.5):
    length = len(strip)
    for i in range(iterations):
        for x in range(2):
            clear(strip)
            for y in range(length):
                if (y % 2) == x:
                    strip[y] = color1
                else:
                    strip[y] = color2
            strip.show()
            time.sleep(wait)

def stagger_chase_clockwise(strip, color, seperation = 3, iterations = 2, wait = 0.5):
    length = len(strip)
    for i in range(iterations):
        for x in range(seperation):
            clear(strip)
            for y in range(length):
                if (y % seperation) == x:
                    strip[y] = color
                else:
                    strip[y] = OFF
            strip.show()
            time.sleep(wait)

def stagger_chase_counterclockwise(strip, color, seperation = 3, iterations = 2, wait = 0.5):
    length = len(strip)
    for i in range(iterations):
        for x in range((seperation - 1), -1, -1):
            clear(strip)
            for y in range(length):
                if (y % seperation) == x:
                    strip[y] = color
                else:
                    strip[y] = OFF
            strip.show()
            time.sleep(wait)

        
def color_chase(strip, color, wait = 0.01, direction = 1):
    length = len(strip)    
    for i in range(length):
        pixel = (i + (length // 2)) % length
        if direction != 1:
            pixel = (length - pixel) % length
        strip[pixel] = color
        time.sleep(wait)
        strip.show()
    time.sleep(0.5)

def shoot_up(strip, color, wait = 0.1):
    length = len(strip)
    strip[0] = color
    strip.show()
    time.sleep(wait)
    for x in range(1, length // 2):
        clear(strip)
        strip[x] = color
        strip[(len(strip) - x) % length] = color
        strip.show()
        time.sleep(wait)
    strip[length // 2] = color
    strip.show()
    time.sleep(wait)

def shoot_up_tail(strip, color, tail_color = RED, wait = 0.05):
    length = len(strip)
    strip[0] = color
    strip.show()
    time.sleep(wait)
    for x in range(1, length // 2):
        clear(strip)
        strip[x] = color
        strip[(length - x) % length] = color
        
        if x > 1:
            strip[x - 1] = dim(tail_color, 75)
            strip[(length - x + 1) % length] = dim(tail_color, 75)
        if x > 2:
            strip[x - 2] = dim(tail_color, 50)
            strip[(length - x + 2) % length] = dim(tail_color, 50)
        if x > 3:
            strip[x - 3] = dim(tail_color, 25)
            strip[(length - x + 3) % length] = dim(tail_color, 25)
        if x > 4:
            strip[x - 4] = dim(tail_color, 10)
            strip[(length - x + 4) % length] = dim(tail_color, 10)

        strip.show()
        time.sleep(wait)

    clear(strip)
    strip[length // 2] = color
    strip.show()
    time.sleep(wait)

def flash_bang(strip, color, wait = 0.03):
    strip.fill(color)
    strip.show()
    time.sleep(wait * 4)
    for x in range(0, 100, 5):
        for y in range(len(strip)):
            strip[y] = dim(color, 100 - x)
        strip.show()
        time.sleep(wait)

def drop_down(strip, color, wait = 0.01):
    length = len(strip)
    strip[length // 2] = color
    strip.show()
    time.sleep(wait)
    for x in range((length // 2) + 1, length):
        clear(strip)
        strip[x] = color
        strip[(len(strip) - x) % length] = color
        strip.show()
        time.sleep(wait)
    clear(strip)
    strip[0] = color
    strip.show()
    time.sleep(wait)

def fill_down(strip, color, wait = 0.001):
    length = len(strip)
    strip[length // 2] = color
    strip.show()
    time.sleep(wait)
    for x in range((length // 2) + 1, length):
        strip[x] = color
        strip[(len(strip) - x) % length] = color
        strip.show()
        time.sleep(wait)
    strip[0] = color
    strip.show()
    time.sleep(wait)

def sparkle_out(strip, color, wait = 0.002):
    length = len(strip)
    for x in range(length):
        for y in range(x // 8):
            clear(strip)
            random_pixels(strip, color, length - x )
            strip.show()
            time.sleep(wait)


def rainbow(strip, wait = 0.01, iterations = 1):
   for j in range(255 * iterations):
      for i in range(len(strip)):
         strip[i] = wheel((i + j) & 255)
      strip.show()
      time.sleep(wait)

def rainbow_cycle(strip, wait = 0.01, iterations = 1):
    for j in range(255 * iterations):
        for i in range(len(strip)):
            rc_index = (i * 256 // len(strip)) + j
            strip[i] = wheel(rc_index & 255)
        strip.show()
        time.sleep(wait)

def rainbow_cycle_fill(strip, wait = 0.0000001, iterations = 1):
    length = len(strip)
    for x in range(length):
        for j in range(0, 255 * iterations, 3):
            for i in range(x):
                i = (i + (length // 2)) % length
                rc_index = (i * 256 // len(strip)) + j
                strip[i] = wheel(rc_index & 255)
            strip.show()
            time.sleep(wait)