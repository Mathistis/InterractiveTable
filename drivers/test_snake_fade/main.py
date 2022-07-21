#!/usr/bin/env python3
import time
import socket
import os
import board
from rpi_ws281x import PixelStrip, Color
from colour import Color as ColorFade

def getRGBfromI(RGBint):
    blue =  RGBint & 255
    green = (RGBint >> 8) & 255
    red =   (RGBint >> 16) & 255
    return green, red, blue

class multi_strip:
    def __init__(self, neopixels):
        self.strips = strips
    
    def turnOff(self):
        self.fill(0)
    
    #show made automatocally
    def fill(self, color):
        for s in self.strips:
            for i in range(s.numPixels()):
                s.setPixelColor(i, color)
        self.show()

    def show(self):
        for s in self.strips:
            s.show()
    
    def test_leds_snake(self):        #supposed to be deleted ...
        counts = [ s.numPixels() for s in self.strips]
        tot = sum(counts)
        j = 0 # actual bus
        for s in strips:
            for i in range(s.numPixels()):
                s.setPixelColor(i, 14066613)
                s.show()

    def test_wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def before_fade(self):
        color = 15597823
        self.fill(color)
        time.sleep(1)
        color = 385791
        self.fill(color)
        time.sleep(1)
        color = 393119
        self.fill(color)
        time.sleep(1)
        color = 12386053
        self.fill(color)
        time.sleep(1)
        color = 16756741
        self.fill(color)
        time.sleep(1)
        color = 16713111
        self.fill(color)
        time.sleep(1)
        self.turnOff()
        time.sleep(1)

    def test_leds_fade(self):        #supposed to be deleted ...
        r = 255
        g = 0
        b = 0
        for i in range(255):
            if r > 0 and b == 0:
                r-=1
                g+=1
            
            if g > 0 and r == 0:
                g-=1
                b+=1
            
            if b > 0 and g == 0:
                r+=1
                b-=1
            color = self.test_wheel(i)
            print(color)
            self.fill(color)

    
LED_FREQ_HZ = 800000
LED_BRIGHTNESS = 2     # Set to in %
LED_INVERT = False


# Create NeoPixel object with appropriate configuration.
strip1 = PixelStrip(2048, 18, LED_FREQ_HZ, 10, LED_INVERT, LED_BRIGHTNESS, 0)
strip2 = PixelStrip(1024, 13, LED_FREQ_HZ, 10, LED_INVERT, LED_BRIGHTNESS, 1)
# Intialize the library (must be called once before other functions).
strip1.begin()
strip2.begin()


# pixels1 = neopixel.Adafruit_NeoPixel(2048, board.D13,LED_FREQ_HZ, LED_DMA, False, LED_BRIGHTNESS/100, LED_CHANNEL)
# pixels2 = neopixel.NeoPixel(board.D18, 1024, brightness=LED_BRIGHTNESS/100, auto_write=True, pixel_order=neopixel.RGB)
strips = [strip1, strip2]

pix = multi_strip(strips)





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

    pix.turnOff()
    pix.test_leds_snake()
    # for i in range (0):
    #     pix.before_fade()
    # pix.test_leds_fade()


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
                if color == 1 :
                    print('-----------------------')
                    print('----Socket closed !----')
                    print('-----------------------')
                    break
                elif color == 2:
                    pix.turnOff()
                elif color > 60 and color < 16777216:
                    pix.fill(getRGBfromI(color))
                    pix.show()
                else:
                    print('NOT DISPLAYED')
                
            client.close()
        socketsnd.close()

    except KeyboardInterrupt:
        client.send((99).to_bytes(2, byteorder='big'))
        pixels1.fill((0, 0, 0))
        pixels1.show()
        pixels2.fill((0, 0, 0))
        pixels2.show()
        print('over')
        client.close()
        socketsnd.close()