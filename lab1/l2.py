import math
import os
import sys


def file_reader(file_name):
    file_entropy = dict()
    file_cond_entropy = dict()
    with open(file_name, "br") as file:
        for line in file:
            for i, c in enumerate(line):
                file_entropy[c] = file_entropy.setdefault(c, 0) + 1
                file_cond_entropy[c, line[i-1]
                                  ] = file_cond_entropy.setdefault((c, line[i-1]), 0) + 1

    bytes_in_file = os.stat(file_name).st_size
    entropy = -1 * sum((single_byte / bytes_in_file) *
                        math.log2(single_byte / bytes_in_file) for single_byte in file_entropy.values())
    cond_entropy = -1 * sum(
        v / bytes_in_file
        * sum(
            vv / v * math.log2(vv / v) for kk, vv in file_cond_entropy.items() if kk[1] == k
        )
        for k, v in file_entropy.items()
    )

    print(entropy)
    print(cond_entropy)


if __name__ == "__main__":
    filename = sys.argv[1]
    file_reader(filename)