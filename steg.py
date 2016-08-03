#! /usr/bin/python3

BITS_PER_VALUE = 1

def encode_value(value, data):
    if data >= 2**BITS_PER_VALUE or data < 0: 
        raise ValueError('Data to encode must be {} bit'.format(BITS_PER_VALUE))

    return value | data
 

print(encode_value(int('F', 16), 2))
