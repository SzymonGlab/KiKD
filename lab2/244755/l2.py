import math
import os
import sys
import copy
import bitstring as bs


class HeapNode:
    n = 256

    def __init__(self, char, weight):
        self.char = char
        self.weight = weight
        self.left = None
        self.right = None
        self.code = ''
        self.parent = None
        self.n = HeapNode.n
        HeapNode.n -= 1

    def increase_weight(self):
        self.weight += 1

    def __repr__(self):
        if self.left is None:
            return f'Char: {(self.char)} Weight: {self.weight} N: {self.n} LEFT: --- RIGHT: ---\n'
        return f'Char: {(self.char)} Weight: {self.weight} N: {self.n} LEFT: {(self.left.char)} - {self.left.n} RIGHT: {(self.right.char)} - {self.right.n}\n'

# Function to parse letter to 8 bit ASCII


def get_fixed_code(letter):
    return bin(letter).replace('0b', '').zfill(8)


def code(file_name):
    with open(file_name, "r") as file:
        text = file.read()
        code = ''
        heap = [HeapNode('NYT', 0)]
        codesInHeap = []
        last_progress = - 1
        for i, c in enumerate(text):

            letter_ascii = ord(c)

            if letter_ascii in codesInHeap:
                code += get_code(letter_ascii, heap)
            else:
                code += get_code('NYT', heap)
                code += get_fixed_code(letter_ascii)
                codesInHeap.append(letter_ascii)

            heap = add_to_heap(letter_ascii, heap)

            # Displaying progress while coding
            progress = round(i*100/len(text))
            if progress > last_progress:
                last_progress = progress
                print(chr(27) + "[2J ", end='')
                print(f"PROGRESS = {round(i*100/len(text))}%")

    return code, heap

# Function adds a letter to tree


def add_to_heap(letter, heap):

    # First occurance of letter
    if letter not in map(lambda x: x.char, heap):
        heap, node = create_new_nodes(heap, letter)
    # Letter was in text before
    else:
        node = next(x for x in heap if x.char == letter)

    validate_tree(node, heap)

    return heap

# BFS


def get_code(letter, heap):

    nodes = [heap[0]]
    node = heap[0]
    while node.char != letter:
        node = nodes.pop(0)

        # Node always has 2 children
        if node.left is not None:
            node.left.code = node.code + '0'
            node.right.code = node.code + '1'
            nodes.extend([node.left, node.right])
    return node.code

# Creates two children nodes of NYT


def create_new_nodes(heap, letter):
    # Get NYT node
    new_parent = next(x for x in heap if x.char == 'NYT')

    # Update NYT node
    new_parent.char = 'temp'
    new_parent.increase_weight()

    # If it wasn't root node, update also info in parent
    if new_parent.parent is not None:
        new_parent.parent.left = new_parent

    # Create 2 new nodes
    new_parent.right = HeapNode(letter, 1)
    new_parent.left = HeapNode('NYT', 0)

    # Update parent of new nodes
    new_parent.left.parent = new_parent
    new_parent.right.parent = new_parent

    # Add new nodes to heap
    heap.extend([new_parent.right, new_parent.left])

    return heap, new_parent.parent

# Checks tree rules


def validate_tree(node, heap):

    # Until node is root
    while node is not None:
        # Get weight block in tree
        weight_group = list(filter(lambda x: x.weight == node.weight, heap))
        weight_group = sorted(weight_group, key=lambda x: x.n, reverse=True)

        # If you can - swap
        if node is not weight_group[0] and node is not weight_group[0].parent and weight_group[0] is not node.parent:
            swap(node, weight_group[0])

        # Update weight
        node.increase_weight()
        node = node.parent


def save_file_bytes(text, file_name):

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


def decode(file_name):

    # Reading bits
    b = bs.ConstBitStream(filename=file_name)
    bitSequence = []
    try:
        print(chr(27) + "[2J ", end='')
        print('READING FILE ...')
        while True:
            bitSequence.append(b.read('uint:1'))
    except bs.ReadError:
        pass

    # Cutting padding
    padding = int("".join(str(x) for x in bitSequence[0:8]), 2)
    bitSequence = bitSequence[8:len(bitSequence)-padding+1]

    code_length = 8
    i = 0
    root = HeapNode('NYT', 0)
    heap = [root]
    currentNode = root
    output = ''
    last_progress = -1

    while i <= len(bitSequence):

        progress = round(i*100/len(bitSequence))

        if progress > last_progress:
            last_progress = progress
            print(chr(27) + "[2J ", end='')
            print(f"PROGRESS = {round(i*100/len(bitSequence))}%")

        # Node is a leaf
        if currentNode.left is None and currentNode.right is None:
            # Add new letter
            if currentNode.char == 'NYT':
                char = int(
                    ''.join(map(str, bitSequence[i: i + code_length])), 2)
                i += code_length
            # Letter is in the heap
            else:
                char = currentNode.char
            add_to_heap(char, heap)
            currentNode = root
            output += chr(char)

        # Traversing tree looking for a leaf
        else:
            if i != len(bitSequence):
                bit = bitSequence[i]
                currentNode = currentNode.left if bit == 0 else currentNode.right
            i += 1
    return output

# Function to swap two nodes


def swap(node1, node2):

    n1_copy = copy.copy(node1)
    n2_copy = copy.copy(node2)

    parent_n1 = n1_copy.parent
    parent_n2 = n2_copy.parent

    if node1.parent.left == node1 and node2.parent.left == node2:
        parent_n1.left, parent_n2.left = parent_n2.left, parent_n1.left
    elif node1.parent.left == node1 and node2.parent.right == node2:
        parent_n1.left, parent_n2.right = parent_n2.right, parent_n1.left
    elif node1.parent.right == node1 and node2.parent.left == node2:
        parent_n1.right, parent_n2.left = parent_n2.left, parent_n1.right
    elif node1.parent.right == node1 and node2.parent.right == node2:
        parent_n1.right, parent_n2.right = parent_n2.right, parent_n1.right

    node2.parent, node1.parent = node1.parent, node2.parent
    node1.n, node2.n = node2.n, node1.n


def calc_stats(heap, start_file, coded_file):
    ent = 0
    nodes = list(filter(lambda node: node.char !=
                        'temp' and node.char != 'NYT', heap))
    with open(start_file, 'r') as f:
        data = f.read()
        text_len = len(data)

    with open(coded_file, 'rb') as f:
        data = f.read()
        code_len = len(data)

    for node in nodes:
        prob = node.weight/text_len
        ent -= node.weight * math.log2(prob)

    avg = 8 * code_len / text_len
    ent = ent / text_len

    return avg, ent


def display_data(start_file, coded_file, heap):

    avg, ent = calc_stats(heap, start_file, coded_file)
    print()
    print(
        f"Compression rate: {os.stat(start_file).st_size/os.stat(coded_file).st_size}")
    print()
    print(f"Average code length: {avg}")
    print()
    print(f"Entropy: {ent}")
    print()
    print(f'Coding efficiency: {ent/avg * 100}%')
    print()


if __name__ == "__main__":

    if len(sys.argv) != 4 or (sys.argv[1] != 'encode' and sys.argv[1] != 'decode'):
        print("-------------------------------------------------------------------------------------------------")
        print("-                                                                                               -")
        print(
            "-                  USAGE: l2.py [encode/decode] [file_to_code] [result]                           -")
        print("-                                                                                               -")
        print("-------------------------------------------------------------------------------------------------")
        exit()

    file1 = sys.argv[2]
    file2 = sys.argv[3]

    if sys.argv[1] == 'encode':
        code, heap = code(file1)
        save_file_bytes(code, file2)
        display_data(file1, file2, heap)

    elif sys.argv[1] == 'decode':
        save_file(decode(file1), file2)
