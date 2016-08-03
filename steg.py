#! /usr/bin/python

from bitarray import bitarray
from PIL import Image
from optparse import OptionParser
import numpy as np


def encode_value(value, data):
    if data >= 2 or data < 0: 
        raise ValueError('Data to encode must be 1 bit')
    if data:
        return value | 1 
    else:
        return value & (value - 1)
        

def get_lsb(byte):
    # TODO: Should incorporate bits_per_value
    return 0x01 & byte

def bool_to_bin(bool):
    if bool: 
        return 1
    return 0

def decode_image(im):
    data = im.getdata()
    bits = bitarray()

    for pixel in data:
        for value in pixel:
            bits.append(bool(get_lsb(value)))

    return bits.tobytes()

def encode_image(im, message):
    bits = bitarray()
    bits.frombytes(message)
    
    data = im.getdata()
    new_data = []
    counter = 0
    for pixel in data:
        newpixel = []
        for value in pixel:
            if counter < bits.length():
                newpixel.append(encode_value(value, bool_to_bin(bits[counter])))
                counter += 1
            elif counter == bits.length():
                newpixel.append(encode_value(value, 0))
            else:
                newpixel.append(value)
        new_data.append(tuple(newpixel))        
    im.putdata(new_data) 

def main(): 
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename")
    parser.add_option("-m", "--message", dest="message")
    (options, args) = parser.parse_args()

    im = Image.open(options.filename)
    
    if 'encode' in args:
        encode_image(im, options.message)
        im.save('encoded_' + options.filename)

    if 'decode' in args:
        print decode_image(im)[:100]
    
    im.close()
    
if __name__ == '__main__':
    main()

