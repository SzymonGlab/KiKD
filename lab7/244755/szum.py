from sys import argv
from bitstring import ConstBitStream as bs, ReadError
from random import random


def save_file(file_name, text):

    new_bytes = [text[i: i + 8] for i in range(0, len(text), 8)]
    bytes_ = bytearray()

    for i in new_bytes:
        bytes_.append(int(i, 2))

    with open(file_name, "wb") as f:
        f.write(bytes(bytes_))


def open_file(file_name):
    b = bs(filename=file_name)
    bitSequence = []
    try:
        while True:
            bitSequence.append(b.read("uint:1"))
    except ReadError:
        pass

    return "".join(map(str, bitSequence))


def switch(bits, probability):
    return ''.join(
        [str(1 - int(bit)) if random() < probability else bit
         for bit in bits])


if __name__ == "__main__":
    input_f = argv[3]
    output_f = argv[2]
    probability = float(argv[1])

    bits = open_file(input_f)
    switched = switch(bits, probability)
    save_file(output_f, switched)
