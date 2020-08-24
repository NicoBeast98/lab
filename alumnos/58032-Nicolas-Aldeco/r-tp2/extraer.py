import argparse
from header import readHeader


def decode(img):
    header = readHeader(img)
    print(header)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", nargs=1, type=str, required=True
    )
    args = parser.parse_args()
    decode(args.file[0])
