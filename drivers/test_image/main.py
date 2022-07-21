#!/usr/bin/env python3
import time
import socket
import os
import board
from rpi_ws281x import PixelStrip, Color
from colour import Color as ColorFade

import imageio.v3 as iio


# TODO: put in in config file !!
LED_FREQ_HZ = 800000
LED_BRIGHTNESS = 35     # Set to in %
LED_INVERT = False
LED_DMA_NUMBER = 10
SQUARE_SIZE = 16

def getRGBfromI(RGBint):
    blue =  RGBint & 255
    green = (RGBint >> 8) & 255
    red =   (RGBint >> 16) & 255
    return green, red, blue



class Strip(PixelStrip):
    def __init__(self, pixelCount, pin, channel, width, height):
        super().__init__(pixelCount, pin, LED_FREQ_HZ, LED_DMA_NUMBER, LED_INVERT, LED_BRIGHTNESS, channel)
        self.width = width
        self.height = height

    def setPixelFromCoordonate(self, line, column, color):
        totNbrColumn = int(self.width/SQUARE_SIZE)
        number_of_complete_columns = (totNbrColumn - 1) - int(column/SQUARE_SIZE)
        assert number_of_complete_columns >= 0, F"Number_of_complete_columns can't be negative {number_of_complete_columns}"
        newCol = column % SQUARE_SIZE


        finalPixelIndex = (self.height - line -1) * SQUARE_SIZE
        finalPixelIndex += number_of_complete_columns * SQUARE_SIZE * (self.height)
        if line %2 == 0:
            newCol = SQUARE_SIZE - newCol -1
        finalPixelIndex += newCol
        # print(F'finalIndex: {finalPixelIndex}, color: {color}, newCol: {newCol}')
        self.setPixelColor(finalPixelIndex, color)
    

    
class interractiveTable:
    def __init__(self):
        strip2 = Strip(2048, 18, 0, SQUARE_SIZE*2, SQUARE_SIZE*4)
        strip1 = Strip(1024, 13, 1, SQUARE_SIZE, SQUARE_SIZE * 4)

        #WARNING THIS PARF IS VERY IMPORTANT
        # You have to construct the folowing line from left to right of you pannel of strip
        self.strips = [strip1, strip2]
        totPixels = 0
        for s in self.strips:
            s.begin()
            totPixels += s.numPixels()
        self.width = 48 #width in pixels
        self.height = 64 #height in pixels
        assert self.width * self.height == totPixels, "Wrong width ou height"
        
        
        self.PANNELHEIGHT = 16 
        self.PANNELWIDTH = 16 

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

    def draw(self, matrix):
        pass

    def _pannelLocation(self, l, c):
        if c % 2 == 0:
            c = 15 - c
        l = 15 - l
        return l ,c


    def _stripIndex(self, column):
        totL = 0 
        i = 0
        for s in self.strips:
            totL += s.width
            if totL > column:
                return i
            i+=1
        return i


    # calculate new column number from the strip where the pixel is located (used width
    # of previous strips)
    def _deduceStripColumnFromStripIndex(self, index, column):
        c = column
        for i in range(0, index):
            c -= self.strips[i].width 
            
        assert c >= 0, F"impossible column number C: Index: {index}, column: {column}'"
        return c

            
            
        return (int(line/self.PANNELHEIGHT), int(column/self.PANNELWIDTH))

    def setPixel(self, line, column, color):
        assert line < self.height, "invalid line number "
        assert column < self.width, "invalid column number "
        stripIndex = self._stripIndex(column)
        newCol = self._deduceStripColumnFromStripIndex(stripIndex, column)
        self.strips[stripIndex].setPixelFromCoordonate(line,newCol,color)
        
    def test_leds_snake(self):        #supposed to be deleted ...
        counts = [ s.numPixels() for s in self.strips]
        tot = sum(counts)
        for line in range(self.height):
            for col in range(self.width):
                self.setPixel(line, col, 14066613)
                time.sleep(0.1)

    def show_image(self, path):
        im = iio.imread(path)
        for i in range(im.shape[0]):
            for j in range(im.shape[1]):
                # print(im.shape)
                # print(im[i,j])
                color = Color(im[i,j,0], im[i,j, 1], im[i,j, 2])
                if color > 0:
                    print(color)
                self.setPixel(i,j,int(color))
        self.show()
                


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
    pix = interractiveTable()
    pix.turnOff()
    # pix.test_leds_snake()
    pix.show_image('test.png')


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
                    pix.fill(color)
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