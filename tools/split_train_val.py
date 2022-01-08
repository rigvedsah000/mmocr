import os.path
import random
import argparse


def parse_args():
    parser = argparse.ArgumentParser('Convert annotation file from CSV to TXT')
    parser.add_argument('input', type=str, help='CSV file path')
    parser.add_argument('output', type=str, help='Output folder path')
    parser.add_argument('ratio', type=float, default=0.1, help='Validation ratio, range = [0,1]')
    args = parser.parse_args()

    return args


def split_train_val():
    args = parse_args()

    in_file = open(args.input, 'r', encoding='utf8')

    out_train = open(os.path.join(args.output, 'gt_mmocr_train.txt'), 'w', encoding='utf8')
    out_val = open(os.path.join(args.output, 'gt_mmocr_val.txt'), 'w', encoding='utf8')

    lines = in_file.readlines()
    in_file.close()

    print('Processing...')
    print(f'Split ratio: {args.ratio}')

    random.shuffle(lines)

    for line in lines[int(args.ratio * len(lines)):]:
        out_train.write(line)

    out_train.close()

    for line in lines[: int(args.ratio * len(lines))]:
        out_val.write(line)

    out_val.close()

    print('Done!')


if __name__ == '__main__':
    split_train_val()
