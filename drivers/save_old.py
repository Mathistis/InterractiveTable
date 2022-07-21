#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
import socket
import os
import board
import neopixel
import argparse

# LED strip configuration:
LED_COUNT      = 2560     # Number of LED pixels.
LED_PIN        = board.D18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def getRGBfromI(RGBint):
    blue =  RGBint & 255
    green = (RGBint >> 8) & 255
    red =   (RGBint >> 16) & 255
    return green, red, blue

def bindeff(socketsnd):
    print('Getting some new colors...')
    try:
        rcv = client.recv(4)
        print("rcv is : " );
        print(rcv);
        response = int.from_bytes(rcv, byteorder = 'little', signed = True)
        print('Valeur reçue:')
        print(response)
        client.send((100).to_bytes(2, byteorder='big'))
        return response
    except socket.error as e:
        return 1
        


# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=0.01, auto_write=False, pixel_order=neopixel.RGB)

    pixels.fill((0, 0, 0))
    pixels.show()

    try:
        print('Application started')
        print('oppenning server')
        socketsnd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketsnd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socketsnd.bind(('', 2018))
        response = 0
        socketsnd.listen(1)
        while True:
            print('listenning port')
            client, address = socketsnd.accept()
            client.setblocking(True)
            client.settimeout(2.0)
            print('SOCKET ACCEPTED !')
            print ("{} connected".format( address ))
            while True:
                color = bindeff(socketsnd)
                if color ==1 :
                    print('-----------------------')
                    print('----Socket closed !----')
                    print('-----------------------')
                    break
                elif color >30 and color < 60:
                    pixels.brightness= (color-30)/30
                    pixels.show()
                elif color == 2:
                    pixels.fill((0, 0 ,0))
                    pixels.show()
                elif color > 60 and color < 16777216:
                    pixels.fill(getRGBfromI(color))
                    pixels.show()
                else:
                    print('NOT DISPLAYED')
                
            client.close()
        socketsnd.close()

    except KeyboardInterrupt:
        client.send((99).to_bytes(2, byteorder='big'))
        pixels.fill((0, 0, 0))
        pixels.show()
        print('over')
        client.close()
        socketsnd.close()