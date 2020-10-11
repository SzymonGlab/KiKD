import sys
from math import floor, log10


def open_file_as_bytes(file_name):
    with open(file_name, "rb") as bits:
        byte_seq = bits.read()

    width = byte_seq[13] * 256 + byte_seq[12]
    height = byte_seq[15] * 256 + byte_seq[14]

    bitmap = byte_seq[18:-26]
    header = byte_seq[:18]
    footer = byte_seq[-26:]
    return header, width, height, bitmap, footer


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


def code(pixels, rb, gb, bb):
    modified_pixels = []
    errors = [0, 0, 0, 0]
    for pixel in pixels:

        red = floor(pixel[0] / (256 / 2 ** rb)) * int(256 / 2 ** rb) + int(
            256 / 2 ** rb / 2
        )
        green = floor(pixel[1] / (256 / 2 ** gb)) * int(256 / 2 ** gb) + int(
            256 / 2 ** gb / 2
        )
        blue = floor(pixel[2] / (256 / 2 ** bb)) * int(256 / 2 ** bb) + int(
            256 / 2 ** bb / 2
        )

        errors[0] += (pixel[0] - red) ** 2
        errors[1] += (pixel[1] - green) ** 2
        errors[2] += (pixel[2] - blue) ** 2
        errors[3] += (
            (pixel[0] - red) ** 2 + (pixel[1] -
                                     green) ** 2 + (pixel[2] - blue) ** 2
        )

        modified_pixels.append(blue)
        modified_pixels.append(green)
        modified_pixels.append(red)

    return modified_pixels, errors


def save_pic(filename, header, modified_pixels, footer):
    with open(f2, "wb") as w:
        w.write(header)
        w.write(bytes(modified_pixels))
        w.write(footer)


def display_stats(errors, pixels):

    print(f"mse: {errors[3]/(3 * len(pixels))}")
    print(f"mse(r): {errors[0]/len(pixels)}")
    print(f"mse(g): {errors[1]/len(pixels)}")
    print(f"mse(b): {errors[2]/len(pixels)}")

    snr = []
    dbSnr = []
    for i, error in enumerate(errors[:3]):
        if error == 0:
            snr.append(0)
            dbSnr.append(0)
        else:
            snr.append(sum([x[i] ** 2 for x in pixels]) / error)
            dbSnr.append(10*log10(snr[i]))

    if errors[3] == 0:
        snr.append(0)
        dbSnr.append(0)
    else:
        snr.append(
            sum([x[0] ** 2 + x[1] ** 2 + x[2] ** 2 for x in pixels]) / errors[3])
        dbSnr.append(10*log10(snr[i]))

    print(f"snr: {snr[3]} ({dbSnr[3]} dB)")
    print(f"snr(r): {snr[0]} ({dbSnr[0]} dB)")
    print(f"snr(g): {snr[1]} ({dbSnr[1]} dB)")
    print(f"snr(b): {snr[2]} ({dbSnr[2]} dB)")


if __name__ == "__main__":
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    rb = int(sys.argv[3], 10)
    gb = int(sys.argv[4], 10)
    bb = int(sys.argv[5], 10)

    header, width, height, bitmap, footer = open_file_as_bytes(f1)
    pixels = read_bitmap(bitmap)
    modified_pixels, errors = code(pixels, rb, gb, bb)
    save_pic(f1, header, modified_pixels, footer)
    display_stats(errors, pixels)
