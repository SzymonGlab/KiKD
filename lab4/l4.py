import math
import os
import sys
import bitstring as bs
from collections import defaultdict
import itertools
from sys import argv
from math import log2, log, inf


def open_file_as_bytes(file_name):
    with open(file_name, 'rb') as bits:
        byte_seq = bits.read()

    width = byte_seq[13] * 256 + byte_seq[12]
    height = byte_seq[15] * 256 + byte_seq[14]

    bitmap = byte_seq[18:-26]
    return bitmap, width, height


def read_bitmap(bitmap, width, height):

    pixel_counter = 0
    pixels = []
    for row in range(height):
        pixels.append([])
        for column in range(width):
            blue = bitmap[pixel_counter]
            green = bitmap[pixel_counter + 1]
            red = bitmap[pixel_counter + 2]
            pixel_counter += 3
            pixels[row].append((red, green, blue))

    return list(reversed(pixels))


def diff(P1, P2):
    return ((P1[0]-P2[0]), (P1[1]-P2[1]), (P1[2]-P2[2]))


def add(P1, P2):
    return ((P1[0]+P2[0]), (P1[1]+P2[1]), (P1[2]+P2[2]))


def div_by_2(P1):
    return ((P1[0]//2), (P1[1]//2), (P1[2]//2))





def s_1(pixels):
    result = []
    for row in range(len(pixels)):
        for column in range(len(pixels[row])):
            W = pixels[row][column - 1] if column > 0 else (0, 0, 0)
            X = pixels[row][column]
            result.append(diff(X, W))
    return result


def s_2(pixels):
    result = []
    for row in range(len(pixels)):
        for column in range(len(pixels[row])):
            N = pixels[row-1][column] if row > 0 else (0, 0, 0)
            X = pixels[row][column]
            result.append(diff(X, N))
    return result


def s_3(pixels):
    result = []
    for row in range(len(pixels)):
        for column in range(len(pixels[row])):
            NW = pixels[row-1][column -
                               1] if row > 0 and column > 0 else (0, 0, 0)
            X = pixels[row][column]
            result.append(diff(X, NW))
    return result


def s_4(pixels):
    result = []
    for row in range(len(pixels)):
        for column in range(len(pixels[row])):
            W = pixels[row][column - 1] if column > 0 else (0, 0, 0)
            N = pixels[row-1][column] if row > 0 else (0, 0, 0)
            NW = pixels[row-1][column -
                               1] if row > 0 and column > 0 else (0, 0, 0)
            X = pixels[row][column]
            result.append(diff(X, diff(add(N, W), NW)))
    return result


def s_5(pixels):
    result = []
    for row in range(len(pixels)):
        for column in range(len(pixels[row])):
            W = pixels[row][column - 1] if column > 0 else (0, 0, 0)
            N = pixels[row-1][column] if row > 0 else (0, 0, 0)
            NW = pixels[row-1][column -
                               1] if row > 0 and column > 0 else (0, 0, 0)
            X = pixels[row][column]
            result.append(diff(X, add(N, div_by_2(diff(W, NW)))))
    return result


def s_6(pixels):
    result = []
    for row in range(len(pixels)):
        for column in range(len(pixels[row])):
            W = pixels[row][column - 1] if column > 0 else (0, 0, 0)
            N = pixels[row-1][column] if row > 0 else (0, 0, 0)
            NW = pixels[row-1][column -
                               1] if row > 0 and column > 0 else (0, 0, 0)
            X = pixels[row][column]
            result.append(diff(X, add(W, div_by_2(diff(N, NW)))))
    return result


def s_7(pixels):
    result = []
    for row in range(len(pixels)):
        for column in range(len(pixels[row])):
            W = pixels[row][column - 1] if column > 0 else (0, 0, 0)
            N = pixels[row-1][column] if row > 0 else (0, 0, 0)
            X = pixels[row][column]
            result.append(diff(X, div_by_2(add(N, W))))
    return result


def s_8(pixels):
    result = []
    for row in range(len(pixels)):
        for column in range(len(pixels[row])):
            W = pixels[row][column - 1] if column > 0 else (0, 0, 0)
            N = pixels[row-1][column] if row > 0 else (0, 0, 0)
            NW = pixels[row-1][column -
                               1] if row > 0 and column > 0 else (0, 0, 0)
            X = pixels[row][column]
            result.append(diff(X, s_8_helper(NW,W,N)))
    return result

def s_8_helper(NW, W, N):
    color_val =[0,0,0]
    for pos in range(3):
        if NW[pos] >= max(W[pos], N[pos]):
            color_val[pos] = max(W[pos], N[pos])
        elif NW[pos] <= min(W[pos], N[pos]):
            color_val[pos] = min(W[pos], N[pos])
        else:
            color_val[pos] = diff(add(W, N), NW)[pos]
    return color_val


def calc_input_total_entropy(pixels):
    freq = defaultdict(int)
    size = 0
    for row in range(len(pixels)):
        for column in range(len(pixels[row])):
            freq[pixels[row][column][0]] += 1
            freq[pixels[row][column][1]] += 1
            freq[pixels[row][column][2]] += 1
            size += 3

    entropy = sum((log2(size) - log2(i)) * i for i in freq.values())

    return entropy / size


def calc_input_color_entropy(pixels, col_num):
    freq = defaultdict(int)
    size = 0
    for row in range(len(pixels)):
        for column in range(len(pixels[row])):
            freq[pixels[row][column][col_num]] += 1
            size += 1

    entropy = sum((log2(size) - log2(i)) * i for i in freq.values())

    return entropy / size


def calc_total_entropy(differences):
    freq = defaultdict(int)
    size = 0
    for diff in differences:
        freq[diff[0]] += 1
        freq[diff[1]] += 1
        freq[diff[2]] += 1
        size += 3

    entropy = sum((log2(size) - log2(i)) * i for i in freq.values())

    return entropy / size


def calc_color_entropy(differences, col_num):
    freq = defaultdict(int)
    size = 0
    for diff in differences:
        freq[diff[col_num]] += 1
        size += 1

    entropy = sum((log2(size) - log2(i)) * i for i in freq.values())

    return entropy / size


def get_best_pred_entropy(pixels):
    s_ = [s_1, s_2, s_3, s_4, s_5, s_6, s_7, s_8]

    best_r = (inf,-1)
    best_g = (inf,-1)
    best_b = (inf,-1)
    best_tot = (inf,-1)

    for i,pred in enumerate(s_):

        p = list(map(lambda x: (x[0]%256,x[1]%256,x[2]%256), pred(pixels)))
        

        new_tot = calc_total_entropy(p)
        new_r = calc_color_entropy(p, 0)
        
        new_g = calc_color_entropy(p, 1)
        new_b = calc_color_entropy(p, 2)

        print()
        print(f'SCHEME {i}')
        print(f'T: {new_tot}')
        print(f'R: {new_r}')
        print(f'G: {new_g}')
        print(f'B: {new_b}')
        print()

        if new_tot < best_tot[0]:
            best_tot = (new_tot,i+1)
        if new_r < best_r[0]:
            best_r = (new_r,i+1)
        if new_g < best_g[0]:
            best_g = (new_g,i+1)
        if new_b < best_b[0]:
            best_b = (new_b,i+1)

    return best_r, best_g, best_b, best_tot


if __name__ == "__main__":
    bitmap, width, height = open_file_as_bytes(argv[1])
    pixels = read_bitmap(bitmap, width, height)

    i_entropy = calc_input_total_entropy(pixels)
    i_ent_r = calc_input_color_entropy(pixels, 0)
    i_ent_g = calc_input_color_entropy(pixels, 1)
    i_ent_b = calc_input_color_entropy(pixels, 2)

    print()
    print(f'INPUT ENTROPY: {i_entropy}')
    print(f'RED: {i_ent_r}')
    print(f'GREEN: {i_ent_g}')
    print(f'BLUE: {i_ent_b}')

    best_r,best_g,best_b, best_tot = get_best_pred_entropy(pixels)

    print(f'BEST PREDICITON GENERAL: SCHEME {best_tot[1]}')
    print(f'BEST PREDICITON RED: SCHEME {best_r[1]}')
    print(f'BEST PREDICITON GREEN: SCHEME {best_g[1]}')
    print(f'BEST PREDICITON BLUE: SCHEME {best_b[1]}')
