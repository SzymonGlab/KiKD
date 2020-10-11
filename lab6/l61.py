import sys
from math import floor


def open_file_as_bytes(file_name):
    with open(file_name, "rb") as bits:
        byte_seq = bits.read()

    bitmap = byte_seq[18:-26]
    header = byte_seq[:18]
    footer = byte_seq[-26:]
    return header, bitmap, footer


def read_bitmap(bitmap):
    pixel_counter = 0
    pixels = []
    while pixel_counter < len(bitmap):
        blue = bitmap[pixel_counter]
        green = bitmap[pixel_counter + 1]
        red = bitmap[pixel_counter + 2]
        pixel_counter += 3
        pixels.append((red, green, blue))
    return pixels


def code(pixels, k):
    i = 0

    X_r = []
    X_g = []
    X_b = []

    D_g = []
    D_b = []
    D_r = []

    def Q(number):
        y = (number / 2) + 128
        x = floor(y / (256 / 2 ** k)) * int(256 / 2 ** k) + int(
            256 / 2 ** k / 2)
        if x == -80:
            print(f'NUMBER: {y}')
            print(x)
        return x

    while i < len(pixels):
        if i == 0:
            D_r.append(Q(pixels[i][0]))
            D_g.append(Q(pixels[i][1]))
            D_b.append(Q(pixels[i][2]))

            X_r.append(D_r[i])
            X_g.append(D_g[i])
            X_b.append(D_b[i])
        else:
            D_r.append(Q(pixels[i][0] - X_r[i-1]))
            D_g.append(Q(pixels[i][1] - X_g[i-1]))
            D_b.append(Q(pixels[i][2] - X_b[i-1]))

            X_r.append(X_r[i-1] + D_r[i])
            X_g.append(X_g[i-1] + D_g[i])
            X_b.append(X_b[i-1] + D_b[i])

        i += 1

    differencesses = []

    for x in range(len(D_r)):
        differencesses.append(D_r[x])
        differencesses.append(D_g[x])
        differencesses.append(D_b[x])

    print(min(differencesses))
    print(max(differencesses))

    return list(map(int, differencesses))


def read_coded_file(coded_differencess):
    differencess = []
    for difference in coded_differencess:
        if difference % 2 == 1:
            differencess.append(-(difference-1)/2)
        else:
            differencess.append(difference/2)

    return list(map(int, differencess))


def decode(differencesses):
    step = 2 ** (8-k)
    d_r = 0
    d_g = 0
    d_b = 0

    pixels = []

    i = 0

    while i < len(differencesses):
        d_r += differencesses[i] * step
        d_g += differencesses[i+1] * step
        d_b += differencesses[i+2] * step

        pixels.append(d_b)
        pixels.append(d_g)
        pixels.append(d_r)

        i += 3

    for i, pixel in enumerate(pixels):
        if pixel == 256:
            pixels[i] = 255

    return pixels


def save_pic(filename, header, modified_pixels, footer):
    with open(f2, "wb") as w:
        w.write(header)
        w.write(bytes(modified_pixels))
        w.write(footer)


def parse_differences(x):
    if x < 0:
        return (2 * (-x)) + 1
    else:
        return 2 * x


if __name__ == "__main__":
    option = sys.argv[1]
    f1 = sys.argv[2]
    f2 = sys.argv[3]
    k = int(sys.argv[4], 10)

    header, bitmap, footer = open_file_as_bytes(f1)

    if option == 'encode':
        pixels = read_bitmap(bitmap)
        differencess = code(pixels, k)
        # positive_differences = list(map(parse_differences, differencess))
        save_pic(f2, header, differencess, footer)
    elif option == 'decode':
        differencess = read_coded_file(bitmap)
        new_pixels = decode(differencess)
        save_pic(f2, header, new_pixels, footer)
