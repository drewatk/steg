#! /usr/bin/python

from bitarray import bitarray
from PIL import Image
import argparse
import os
import warnings

def encode_value(value, data):
    if data >= 2 or data < 0: 
        raise ValueError('Data to encode must be 1 bit')
    if data:
        return value | 1 
    else:
        return value & (value - 1)
        

def get_lsb(byte):
    return 0x01 & byte

def bool_to_bin(boolean):
    if boolean: 
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
    if counter < bits.length():
        warnings.warn("The data too large for image, only stored {:,} bits out of {:,}".format(counter, bits.length()))
    im.putdata(new_data) 

def main():
    parser = argparse.ArgumentParser()
    
    subparsers = parser.add_subparsers(dest='command')

    parser_decode = subparsers.add_parser('decode', help="Decode an image")
    parser_decode.add_argument("file", help="PNG file to decode")

    parser_encode = subparsers.add_parser('encode', help="Encode an image")
    parser_encode.add_argument("-o", "--outputfile", help="Specify output file for endoded Image")
    parser_encode.add_argument("file", help="PNG file to encode")
    parser_encode.add_argument("message", help="Data to encode as file or string")

    args = parser.parse_args()
    
    if args.command == 'encode':
        if os.path.isfile(args.message):
            f = open(args.message, 'r')
            args.message = f.read()

        im = Image.open(args.file)
        im = im.convert('RGB')

        encode_image(im, args.message)

        if args.outputfile:
            im.save(args.outputfile, compress_level=0)
            print "Encoded image saved as " + args.outputfile
        else:
            im.save('encoded_' + args.file, compress_level=0)
            print "Encoded image saved as " + 'encoded_' + args.file
        im.close()

    elif args.command == 'decode':
        im = Image.open(args.file)
        im = im.convert('RGB')
        print decode_image(im)
        im.close()
      
if __name__ == '__main__':
    main()
