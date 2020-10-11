import math
import os
import sys
import bitstring as bs


def code(file_name, dictionary):
    with open(file_name, "r") as file:
        text = file.read()
        codes= []
        text = 'ABABABABABABBB'
        current_char = 0

        while current_char < len(text):
            dictionary, skipped_letters, code = get_prefix(
                text, current_char, dictionary)
            current_char += skipped_letters
            codes.append(code)

        print(dictionary)
        print(codes)


def get_prefix(text, current_position, dictionary):
    skipped_letters = 1
    while text[current_position:current_position + skipped_letters] in dictionary.values():
        if current_position+skipped_letters == len(text):
            prefix_index = list(dictionary.values()).index((text[current_position:current_position+skipped_letters]))
            # dictionary['EOF'] = prefix_index
            return dictionary, skipped_letters, prefix_index
        skipped_letters += 1
    print(f'PREFIX: {text[current_position:current_position+skipped_letters]} SKIPPED LETTERS: {skipped_letters}')
    prefix_index = list(dictionary.values()).index((text[current_position:current_position+skipped_letters-1]))
    dictionary[len(dictionary)] = text[current_position:current_position+skipped_letters]

    return dictionary, skipped_letters - 1, prefix_index


def decode(file_name,dictionary):
    with open(file_name, "r") as file:
        code = file.read()
        # code = [65,66,257,259,258,261]
        code = [65, 66, 257, 259, 258, 261, 66, 66]
        current_char = 1   
        new_code = dictionary.get(code[0])
        dictionary[len(dictionary)] = new_code
        while current_char < len(code):
            dictionary = get_letters(code, current_char, dictionary)
            current_char += 1
        print(dictionary)

        

def get_letters(text, current_position, dictionary):
    letter_code = text[current_position]
    print(f'CODE: {text[current_position]}')
    print(f'DICT LEN: {len(dictionary)} ')
    # If we havent ended decoding this letter_code (It must be the last item in dictionary) => Take first letter of not known yet code and add it to the end
    if letter_code == len(dictionary)-1:
        print(f'ADDING SECOND PART OF CODE AT {len(dictionary)-1} : {dictionary.get(len(dictionary)-1)} + {dictionary.get(len(dictionary)-1)[0:1]}')
        dictionary[len(dictionary)-1] = dictionary.get(len(dictionary)-1) + dictionary.get(text[current_position-1])[0:1]
        dictionary[len(dictionary)] = dictionary[len(dictionary)-1]
        return dictionary


    # Take fiest char of code at given index and put it to previously decoded code,
    # take whole code and put it in next code
    if letter_code in dictionary.keys():
        new_code = dictionary.get(letter_code)
        print(f'ADDING AT {len(dictionary)-1} : {dictionary[len(dictionary)-1]} + {new_code[0:1]} AND CREATING NEW CODE AT {len(dictionary)} : {new_code} ')
        dictionary[len(dictionary)-1] = dictionary.get(len(dictionary)-1) + new_code[0:1]
        dictionary[len(dictionary)] = new_code
        return dictionary

    

if __name__ == "__main__":
    
    ascii_dict = dict()
    ascii_in_number = range(0,257)
    for i in ascii_in_number:
        ascii_dict[i] = chr(i)
    decode('1', ascii_dict)
    # print(ascii_dict)
    # if len(sys.argv) != 4:
    #     print("-------------------------------------------------------------------------------------------------")
    #     print("-                                                                                               -")
    #     print("-                  USAGE: l2.py [code/decode] [file_to_code] [result]                           -")
    #     print("-                                                                                               -")
    #     print("-------------------------------------------------------------------------------------------------")
    #     exit()

    # file1 = sys.argv[2]
    # file2 = sys.argv[3]

    # if sys.argv[1] == 'code':
    #     save_file_bytes(code(file1,file2),file2)

    # elif sys.argv[1] == 'decode':
    #     save_file(decode(file1),file2)

    # else:
    #     print()
    #     print("Use CODE or DECODE option.")
    #     print()
