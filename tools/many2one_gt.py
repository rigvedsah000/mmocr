import os
import argparse
import random


def parse_args():
    parser = argparse.ArgumentParser('Convert annotation file from CSV to TXT')
    parser.add_argument('input', type=str, help='CSV file path')
    parser.add_argument('output', type=str, help='Output folder path')
    args = parser.parse_args()

    return args


def many2one_get():
    args = parse_args()

    print('Starting...')

    files = os.listdir(args.input)
    out_file = open(os.path.join(args.output, 'gt.txt'), 'w', encoding='utf8')

    for filename in files:
        if filename.endswith(".txt"):

            in_file = open(os.path.join(args.input, filename), encoding='utf8')

            print(f'Processing {filename}')

            for line in in_file.readlines():
                out_file.write(line)

            in_file.close()

    out_file.close()
    print('Done!')


if __name__ == '__main__':
    many2one_get()