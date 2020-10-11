from sys import argv
from bitstring import ConstBitStream as bs, ReadError


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


def calc_diff(bits1, bits2):
    diffs = 0
    for x in range(4, len(bits1)+1, 4):
        if(bits1[x-4:x] != bits2[x-4:x]):
            diffs += 1

    return diffs


if __name__ == "__main__":
    input_f1 = argv[1]
    input_f2 = argv[2]

    bits1 = open_file(input_f1)
    bits2 = open_file(input_f2)

    diffs = calc_diff(bits1, bits2)

    print(f'Znaleziono {diffs} różnice')
