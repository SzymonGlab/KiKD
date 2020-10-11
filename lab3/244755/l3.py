import math
import os
import sys
import bitstring as bs
from collections import defaultdict
import itertools


def encode(text):
    p = ''
    code = 257
    # Create default ascii dict
    codes_array = {chr(i): i for i in range(0, 256)}
    codes = []
    c = ''
    p += chr(text[0])

    for i in range(0, len(text)):
        if i != len(text) - 1:
            c += chr(text[i+1])
        if p + c in codes_array.keys():
            p = p + c
        else:
            codes.append(codes_array[p])
            codes_array[p+c] = code
            code += 1
            p = c
        c = ''
    codes.append(codes_array[p])

    return codes


def get_prefix(text, start_position, dictionary):
    read_letters = 1
    code = text[start_position:start_position+read_letters]

    while code in dictionary.values():
        # If we are reading last letter of code, return return the code saved in dictionary
        if start_position + read_letters > len(text):
            code_value = list(dictionary.values()).index(code)
            return dictionary, read_letters, code_value

        read_letters += 1
        code = text[start_position:start_position+read_letters]

    prefix = text[start_position:start_position+read_letters-1]
    prefix_index = list(dictionary.values()).index(prefix)
    # Create new code in dictionary
    code_index = len(dictionary)
    dictionary[code_index] = code

    return dictionary, read_letters, prefix_index


def decode(code):

    codes_array = {i: chr(i) for i in range(0, 256)}
    old = code[0]
    s = codes_array[old]
    c = s[0]
    count = 257
    text = [c]

    for i in range(0, len(code)-1):
        n = code[i+1]
        if n not in codes_array.keys():
            s = codes_array[old]
            s = s + c
        else:
            s = codes_array[n]
        text.append(s)
        c = s[0]
        codes_array[count] = codes_array[old] + c
        count += 1
        old = n

    return ''.join(text)


def get_letters(text, current_position, dictionary):
    letter_code = text[current_position]
    # If we havent ended decoding this letter_code (It must be the last item in dictionary) => Take first letter of not known yet code and add it to the end
    if letter_code == len(dictionary)-1:
        dictionary[len(dictionary)-1] = dictionary.get(len(dictionary) -
                                                       1) + dictionary.get(text[current_position-1])[0:1]
        dictionary[len(dictionary)] = dictionary[len(dictionary)-1]
        return dictionary

    # Take fiest char of code at given index and put it to previously decoded code,
    # take whole code and put it in next code
    if letter_code in dictionary.keys():
        new_code = dictionary.get(letter_code)
        dictionary[len(dictionary) -
                   1] = dictionary.get(len(dictionary)-1) + new_code[0:1]
        dictionary[len(dictionary)] = new_code
        return dictionary


def save_file_as_bytes(text, file_name):

    print(f'CODE LENGTH: {len(text)}')

    padding_counter = 0

    # Add padding
    while len(text) % 8 != 0:
        text += '0'
        padding_counter += 1

    # Save padding as first bit
    text_with_padding = bin(padding_counter).replace('b', '').zfill(8) + text

    # Save bits to file
    new_bytes = [text_with_padding[i:i+8]
                 for i in range(0, len(text_with_padding), 8)]
    bytes_ = bytearray()

    for i in new_bytes:
        bytes_.append(int(i, 2))

    with open(file_name, 'wb') as f:
        f.write(bytes(bytes_))


def save_file(text, file_name):
    with open(file_name, 'w') as f:
        f.write(text)


def open_file_as_bytes(file_name):
    b = bs.ConstBitStream(filename=file_name)
    bitSequence = []
    try:
        while True:
            bitSequence.append(b.read('uint:1'))
    except bs.ReadError:
        pass

    # Cutting padding
    padding = int("".join(str(x) for x in bitSequence[0:8]), 2)
    bitSequence = bitSequence[8:len(bitSequence)-padding]

    return "".join(map(str, bitSequence))


def open_file(file_name):
    with open(file_name, 'rb') as file:
        text = file.read()
        print(f'TEXT LENGTH: {len(text)}')
    return text


def fibb_encoding(code):

    fibb_numbers = [1, 1]
    bits = []

    for number in code:
        # Code length
        first_1_pos, fibb_numbers = get_fibb_position(number, fibb_numbers)
        number_code = [0 for x in range(0, first_1_pos)]
        number_code[0] = 1

        number -= fibb_numbers[first_1_pos]

        # Array of fibbonacci numbers containing only numbers smaller then current number
        temp_fibb_array = fibb_numbers[:first_1_pos+1]

        for i, fibb_number in enumerate(reversed(temp_fibb_array)):
            if number > 0 and number >= fibb_number:
                number -= fibb_number
                number_code[i] = 1

        # Reverse code and add '1'
        number_code = list(reversed(number_code))
        number_code.append(1)

        # Add coded number to bits array
        bits.append(''.join(map(str, number_code)))

    return ''.join(bits)


def get_fibb_position(number, fibb_array):
    if number <= fibb_array[len(fibb_array)-1]:
        number_index = next(fibb_array.index(x)
                            for x in fibb_array if x > number)
        return number_index - 1, fibb_array
    else:
        # Number is bigger than biggest number in array, so on start it has array length position
        current_position = len(fibb_array) - 1
        while number >= fibb_array[len(fibb_array)-1]:
            new = fibb_array[len(fibb_array)-2] + fibb_array[len(fibb_array)-1]
            fibb_array.append(new)
            current_position += 1

    return current_position - 1, fibb_array


def parse_code_fibb(bits, fibb_numbers):
    decoded_number = 0
    # In array there are two '1' at start, in coding we start with one '1'
    if len(bits) > len(fibb_numbers) - 1:
        while len(fibb_numbers) - 1 < len(bits):
            fibb_numbers.append(
                fibb_numbers[len(fibb_numbers)-2] + fibb_numbers[len(fibb_numbers)-1])

    for i, bit in enumerate(bits):
        if bit == '1':
            decoded_number += fibb_numbers[i+1]
    return decoded_number, fibb_numbers


def fibb_decoding(bits):

    fibb_numbers = [1, 1]
    code = []
    number_end = 1
    while len(bits) > 0:
        while bits[:number_end][-2:] != '11':
            number_end += 1

        # Cut second '1' from coded number
        decoded_number, fibb_numbers = parse_code_fibb(
            bits[:number_end-1], fibb_numbers)

        bits = bits[number_end:]
        number_end = 0
        code.append(decoded_number)

    return code


def gamma_encoding(code):

    bits = []
    for number in code:
        bin_representation = bin(number)[2:]
        z_prefix = len(bin_representation)

        bit_representation = ['0' for x in range(1, z_prefix)]
        bit_representation.extend(bin_representation)

        bit_representation = ''.join(map(str, bit_representation))

        bits.append(bit_representation)
    return ''.join(bits)


def gamma_decoding(bits):

    z_counter = 1
    code = []
    while len(bits) > 0:
        # Read until you get 1
        while bits[:z_counter][-1:] != '1':
            z_counter += 1

        # Cut zeros part
        bits = bits[z_counter-1:]
        number = int(bits[:z_counter], 2)
        bits = bits[z_counter:]
        z_counter = 0
        code.append(number)

    return code


def delta_encoding(code):
    bits = []
    for number in code:
        n = math.floor(math.log2(number))
        number = number - 2**n
        prefix = gamma_encoding([n+1])
        sufix = str(bin(number)[2:])
        while len(sufix) != n:
            sufix = '0' + sufix

        code = prefix + sufix

        bits.append(code)

    return ''.join(bits)


def delta_decoding(bits):

    code = []

    while len(bits) > 0:
        z_counter = 0
        # Read until you get 1
        while bits[:z_counter][-1:] != '1':
            z_counter += 1

        z_counter -= 1
        n = int(bits[:2*z_counter+1], 2) - 1
        sec_part = int(bits[2*z_counter+1:2*z_counter+n+1], 2)
        code.append(2**n+sec_part)
        bits = bits[2*z_counter+n+1:]

    return code


def omega_encoding(code):
    bits = []

    for number in code:
        number_bits = '0'

        while number != 1:
            bin_repr = bin(number)[2:]
            number = len(bin_repr) - 1
            number_bits = ''.join(map(str, bin_repr)) + number_bits

        bits.append(number_bits)
    return ''.join(bits)


def omega_decoding(bits):

    code = []
    n = 1
    current_position = 0

    while current_position < len(bits):
        if bits[current_position] == '0':
            code.append(n)
            current_position += 1
            n = 1
        else:

            tmp = n
            n = int(bits[current_position: current_position+n+1], 2)
            current_position += tmp+1

    return code


def print_entropy(file_name):
    entropy = 0
    with open(file_name, "br") as file:
        text = file.read()
        occ = {}
        for i in range(0, len(text)-1):
            if text[i] not in occ:
                occ[text[i]] = 0
            occ[text[i]] += 1

    bytes_in_file = os.stat(file_name).st_size
    log_bytes_in_file = math.log2(bytes_in_file)

    for byte_freq in occ.values():
        entropy += -(math.log2(byte_freq) - log_bytes_in_file) * byte_freq
        entropy /= bytes_in_file
    return entropy


def print_compression_rate(file1, file2):
    print(f"Compression rate: {os.stat(file1).st_size/os.stat(file2).st_size}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("-------------------------------------------------------------------------------------------------")
        print("-                                                                                               -")
        print(
            "-                  USAGE: l3.py [-g/-d/-o-fibb] [encode/decode] [file_to_code] [result]                           -")
        print("-                                                                                               -")
        print("-------------------------------------------------------------------------------------------------")
        exit()

    opt = sys.argv[1]
    file1 = sys.argv[3]
    file2 = sys.argv[4]

    if sys.argv[2] == 'encode':
        text = open_file(file1)
        code = encode(text)

        if opt == '-fibb':
            bits = fibb_encoding(code)
        elif opt == '-g':
            bits = gamma_encoding(code)
        elif opt == '-d':
            bits = delta_encoding(code)
        elif opt == '-o':
            bits = omega_encoding(code)

        save_file_as_bytes(bits, file2)
        print_compression_rate(file1, file2)
        input_ent = print_entropy(file1)
        print(f'INPUT ENTROPY: {input_ent}')
        output_ent = print_entropy(file2)
        print(f'OUTUPT ENTROPY: {output_ent}')

    elif sys.argv[2] == 'decode':
        bits = open_file_as_bytes(file1)

        if opt == '-fibb':
            code = fibb_decoding(bits)
        elif opt == '-g':
            code = gamma_decoding(bits)
        elif opt == '-d':
            code = delta_decoding(bits)
        elif opt == '-o':
            code = omega_decoding(bits)

        text = decode(code)
        save_file(text, file2)

    else:
        print("-------------------------------------------------------------------------------------------------")
        print("-                                                                                               -")
        print(
            "-                  USAGE: l3.py [encode/decode] [file_to_code] [result]                           -")
        print("-                                                                                               -")
        print("-------------------------------------------------------------------------------------------------")
        exit()
