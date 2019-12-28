#!/usr/bin/python3

try:
    import time
    import board
    import neopixel
    import subprocess as sub
    import sys
    import signal
    import argparse
    from random import randint

    from strip_lib.led_strip import *
except Exception as err:
    print >> sys.stderr, err
    sys.exit(1)

STRIP_SIZE = 60
PI_PIN = board.D18
ORDER = neopixel.GRB
BRIGHTNESS = 0.8

global ORIGIN, DIRECTION, TEST
ORIGIN = 30 # Set the default 12-o-clock position
DIRECTION = 1 # Set the default direction - 1 = 0 -> length, 2 = length -> 0
TEST = 0

## Clock Colors
H_HAND = GREEN
M_HAND = BLUE
S_HAND = RED
HS_MATCH = YELLOW
HM_MATCH = CYAN
MS_MATCH = PURPLE
FULL_MATCH = WHITE

## Signal Handling
def sigterm_handler(signal, frame):
    print("\n\n[*] Exiting...")
    close_strip(clock)
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

### Clock Functions

## Get time from OS
def get_time():
  out, error = sub.Popen(["date +'%I %M %S'"], stdout=sub.PIPE, stderr=sub.PIPE, shell=True).communicate()
  time_raw = out.decode('utf-8').strip().split(' ')
  hours = int(time_raw[0])
  minutes = int(time_raw[1])
  seconds = int(time_raw[2])
  return (hours, minutes, seconds)

## Adjust clock based on ORIGIN pixel and clock direction
def shift(pixel):
    out_pixel = (pixel + ORIGIN) % STRIP_SIZE
    if DIRECTION == 2:
        return (STRIP_SIZE - out_pixel) % STRIP_SIZE
    else:
        return out_pixel

## Show the time on the clock
def show_time(strip):
    clear(strip)
    hours, minutes, seconds = get_time()
    hours = (hours * 5) % len(strip)
    if (hours == minutes) and (minutes != seconds):
        hour_min_match(strip, hours)
        strip[shift(seconds)] = S_HAND
    elif (hours == seconds) and (hours != minutes):
        hour_sec_match(strip, hours)
        strip[shift(minutes)] = M_HAND
    elif (minutes == seconds) and (hours != minutes):
        if minutes == 0:
            random_hour_chime(strip)
        else:
            min_sec_match(strip, minutes)
            strip[shift(hours)] = H_HAND
    elif (hours == minutes) and (hours == seconds):
        if hours == 0:
            random_hour_chime(strip)
        else:
            full_match(strip, hours)
    else:
        strip[shift(hours)] = H_HAND
        strip[shift(minutes)] = M_HAND
        strip[shift(seconds)] = S_HAND
    
    #if seconds == 0: # Chime testing
    #    random_hour_chime(strip)
    
    strip.show()
    time.sleep(0.1)

def hour_min_match(strip, pixel):
    strip[shift(pixel)] = HM_MATCH

def hour_sec_match(strip, pixel):
    strip[shift(pixel)] = HS_MATCH

def min_sec_match(strip, pixel):
    strip[shift(pixel)] = MS_MATCH

def full_match(strip, pixel):
    strip[shift(pixel)] = FULL_MATCH

## Main clock loop
def run_clock(strip):
    if TEST == 1:
        test1(strip)
    if TEST == 2:
        test2(strip)
    else:
        while True:
            show_time(strip)

### Testing Functions
def test1(strip):
    color_chase(strip, RED, wait = 0.005, hold = 0.005, direction = DIRECTION)
    color_chase(strip, ORANGE, wait = 0.005, hold = 0.005, direction = DIRECTION)
    color_chase(strip, YELLOW, wait = 0.005, hold = 0.005, direction = DIRECTION)
    color_chase(strip, GREEN, wait = 0.005, hold = 0.005, direction = DIRECTION)
    color_chase(strip, CYAN, wait = 0.005, hold = 0.005, direction = DIRECTION)
    color_chase(strip, BLUE, wait = 0.005, hold = 0.005, direction = DIRECTION)
    color_chase(strip, PURPLE, wait = 0.005, hold = 0.005, direction = DIRECTION)
    rainbow(strip, wait = 0.01, iterations = 1)

    time.sleep(2)
    close_strip(strip)

def test2(strip):
    rainbow_fill_flash_chime(strip)

### Hour Chimes

## Select random hour chime
def random_hour_chime(strip):
    clear(strip)
    chime_count = 3
    selection = randint(1, chime_count)
    if selection == 1:
        rainbow_fill_flash_chime(strip)
    if selection == 2:
        fireworks(strip, BLUE)
    if selection == 3:
        fireworks(strip, GREEN)

def rainbow_fill_flash_chime(strip):
    rainbow_cycle_fill(strip)
    flash_bang(strip, WHITE)

def fireworks(strip, color):
    shoot_up_tail(strip, color, RED)
    fill_down(strip, color)
    sparkle_out(strip, color)

def parse_args(args, parser):
    global ORIGIN, DIRECTION, TEST

    if args.origin:
        ORIGIN = args.origin

    if args.direction:
        DIRECTION = args.direction

    if args.test:
        TEST = args.test

# Ref to main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "3D Printed LED Clock.")
    parser.add_argument("-o", "--origin", type = int, help = "Origin Pixel - ie. The twelve-o-clock position. Default = 30")
    parser.add_argument("-d", "--direction", type = int, choices = [1, 2], help = "Pixel direction: 1 = positive, 2 = negative. Switch if your clock is going the wrong way. Default = 1")
    parser.add_argument("-t", "--test", type = int, help = "Test Cycle - Testing only.")

    args = parser.parse_args()
    parse_args(args, parser)

    try:
        clock = neopixel.NeoPixel(PI_PIN, STRIP_SIZE, brightness=BRIGHTNESS, auto_write=False, pixel_order=ORDER)
        run_clock(clock)
        close_strip(clock)
    except KeyboardInterrupt:
        print("\n\n[*] Exiting...")
        close_strip(clock)
        sys.exit(3)