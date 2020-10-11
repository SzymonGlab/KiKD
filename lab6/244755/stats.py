import sys
from math import log10, inf


def open_file_as_bytes(file_name):
    with open(file_name, "rb") as bits:
        byte_seq = bits.read()

    bitmap = byte_seq[18:-26]

    return bitmap


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


def count_error(pixels1, pixels2):
    errors = [0, 0, 0, 0]
    for i in range(len(pixels1)):

        errors[0] += (pixels1[i][0] - pixels2[i][0]) ** 2
        errors[1] += (pixels1[i][1] - pixels2[i][1]) ** 2
        errors[2] += (pixels1[i][2] - pixels2[i][2]) ** 2
        errors[3] += (
            (pixels1[i][0] - pixels2[i][0]) ** 2 + (pixels1[i][1] -
                                                    pixels2[i][1]) ** 2 +
            (pixels1[i][2] - pixels2[i][2]) ** 2
        )

    return errors


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
            snr.append(inf)
            dbSnr.append(inf)
        else:
            snr.append(sum([x[i] ** 2 for x in pixels]) / error)
            dbSnr.append(10*log10(snr[i]))

    if errors[3] == 0:
        snr.append(inf)
        dbSnr.append(inf)
    else:
        snr.append(
            sum([x[0] ** 2 + x[1] ** 2 + x[2] ** 2 for x in pixels])
            / errors[3])
        dbSnr.append(10*log10(snr[i]))

    print(f"snr: {snr[3]} ({dbSnr[3]} dB)")
    print(f"snr(r): {snr[0]} ({dbSnr[0]} dB)")
    print(f"snr(g): {snr[1]} ({dbSnr[1]} dB)")
    print(f"snr(b): {snr[2]} ({dbSnr[2]} dB)")


if __name__ == "__main__":
    f1 = sys.argv[1]
    f2 = sys.argv[2]

    bitmap1 = open_file_as_bytes(f1)
    bitmap2 = open_file_as_bytes(f2)
    pixels1 = read_bitmap(bitmap1)
    pixels2 = read_bitmap(bitmap2)
    errors = count_error(pixels1, pixels2)
    display_stats(errors, pixels1)
