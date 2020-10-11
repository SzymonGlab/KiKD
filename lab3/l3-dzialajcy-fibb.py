import math
import os
import sys
import bitstring as bs
import itertools


def code(text):

    # Create default ascii dict
    ascii_dict = dict()
    ascii_in_number = range(0, 256)
    for i in ascii_in_number:
        ascii_dict[i] = chr(i)

    code_start_index = 0
    codes = []

    while code_start_index < len(text):
        ascii_dict, read_letters, code = get_prefix(
            text, code_start_index, ascii_dict)

        code_start_index += read_letters - 1
        codes.append(code)

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
    # print(f'PREFIX: {prefix} READ LETTERS: {read_letters} NEW CODE: {code} NEW CODE INDEX: {code_index}')
    # print(f'ADDED CODES: {dict(list(dictionary.items())[256:])}')

    return dictionary, read_letters, prefix_index

def decode(code):

    ascii_dict = dict()
    ascii_in_number = range(0, 256)

    for i in ascii_in_number:
        ascii_dict[i] = chr(i)

    current_char = 1
    new_code = ascii_dict.get(code[0])
    ascii_dict[len(ascii_dict)] = new_code
    while current_char < len(code):
        ascii_dict = get_letters(code, current_char, ascii_dict)
        current_char += 1

    text = [ascii_dict[number] for number in code]

    return ''.join(text)
    # for number in code:
    #     text += dictionary[code]

def get_letters(text, current_position, dictionary):
    letter_code = text[current_position]
    print(dict(list(dictionary.items())[256:]) )
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

    return "".join(map(str,bitSequence))

def open_file(file_name):
    with open(file_name, 'r') as file:
        text = file.read()
    return text

def fibb_encoding(code):

    fibb_numbers = [1,1]
    bits = []
    

    for number in code:
        print(code)
        print(f'NUMBER: {number}')
        # Code length
        first_1_pos, fibb_numbers = get_fibb_position(number, fibb_numbers)
        print(f"FIB POS = {first_1_pos}")
        number_code = [0 for x in range(0, first_1_pos)]
        number_code[0] = 1

        number -= fibb_numbers[first_1_pos]

        # Array of fibbonacci numbers containing only numbers smaller then current number
        temp_fibb_array = fibb_numbers[:first_1_pos+1]
        print(f'TEMP FIBB ARRAY {temp_fibb_array}')

        for i,fibb_number in enumerate(reversed(temp_fibb_array)):
            if number > 0 and number >= fibb_number:
                print(f'NUMBER: {number} NUMBER CODE: {number_code} i = {i}')
                number -= fibb_number
                number_code[i] = 1
                print(f'NUMBER: {number} NUMBER CODE: {number_code} i = {i}')

        # Reverse code and add '1'    
        number_code = list(reversed(number_code))
        number_code.append(1)

        # Add coded number to bits array
        bits.append(''.join(map(str,number_code)))

        print(f'NUMBER: {number} CODE {"".join(map(str,number_code))}')


    return ''.join(bits)

def get_fibb_position(number, fibb_array):
    if number <= fibb_array[len(fibb_array)-1]:
        number_index = next(fibb_array.index(x) for x in fibb_array if x > number)
        return number_index - 1, fibb_array
    else:
        # Number is bigger than biggest number in array, so on start it has array length position
        current_position = len(fibb_array) - 1
        while number >= fibb_array[len(fibb_array)-1]:
            new = fibb_array[len(fibb_array)-2] + fibb_array[len(fibb_array)-1]
            fibb_array.append(new)
            current_position += 1 
    
    return current_position - 1, fibb_array


def get_number(bits, fibb_numbers):
        decoded_number = 0
        # In array there are two '1' at start, in coding we start with one '1'
        if len(bits) > len(fibb_numbers) - 1:
            while len(fibb_numbers) - 1 < len(bits):
                fibb_numbers.append(fibb_numbers[len(fibb_numbers)-2] + fibb_numbers[len(fibb_numbers)-1])          

        print(fibb_numbers)

        for i,bit in enumerate(bits):
                if bit == '1':
                    decoded_number += fibb_numbers[i+1]
        return decoded_number, fibb_numbers

def fibb_decoding(bits):

    fibb_numbers = [1,1]
    code = []
    number_end = 1
    while len(bits) > 0:
        # print(bits)
        while bits[:number_end][-2:] != '11':
            number_end += 1
    
        print(f'NUMBER END: {number_end}')
        print(bits[:number_end-1])
        # Cut second '1' from coded number 
        decoded_number, fibb_numbers = get_number(bits[:number_end-1], fibb_numbers)
        
        bits = bits[number_end:]
        number_end = 0
        print(f'DECODED NUMBER: {decoded_number}')
        code.append(decoded_number)

    return code




def gamma_encoding(code):
    return bits

def gamma_decoding(code):
    return bits

def delta_encoding(code):
    return bits

def delta_decoding(code):
    return bits

def omega_encoding(code):
    return bits

def omega_decoding(code):
    return bits

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
        code = code(text)
        print(code)
        
        if opt =='-fibb':
            bits = fibb_encoding(code)
        elif opt =='-g':
            bits = gamma_encoding(code)
        elif opt =='-d':
            bits = delta_encoding(code)
        elif opt =='-o':
            bits = omega_encoding(code)
        
        save_file_as_bytes(bits, file2)

    elif sys.argv[2] == 'decode':
        bits = open_file_as_bytes(file1)

        if opt =='-fibb':
            code = fibb_decoding(bits)
        elif opt =='-g':
            code = gamma_decoding(bits)
        elif opt =='-d':
            code = delta_decoding(bits)
        elif opt =='-o':
            code = omega_decoding(bits)
        
        text = decode(code)
        save_file(text,file2)


    else:
        print("-------------------------------------------------------------------------------------------------")
        print("-                                                                                               -")
        print(
            "-                  USAGE: l3.py [encode/decode] [file_to_code] [result]                           -")
        print("-                                                                                               -")
        print("-------------------------------------------------------------------------------------------------")
        exit()
