# Convert to format supported by MMOCR

import pandas as pd
import json
import cv2
import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser('Convert annotation file from CSV to TXT')
    parser.add_argument('input', type=str, help='CSV file path')
    parser.add_argument('imgs', type=str, help='Images folder path')
    parser.add_argument('output', type=str, help='Output folder path')
    args = parser.parse_args()

    return args


def csv2txt():
    args = parse_args()

    df = pd.read_csv(args.input, delimiter='\t', header=None, engine='python')
    f_out = open(os.path.join(args.output, 'gt_mmocr.txt'), 'w')

    total = len(df[0].unique())

    print('Starting...')

    for i, file_name in enumerate(df[0].unique()):

        img = cv2.imread(os.path.join(args.imgs, file_name.split('/')[1]))

        data = dict(file_name=file_name.split('/')[1], height=img.shape[0], width=img.shape[1])
        ann = []

        for row in df.loc[df[0] == file_name].iterrows():
            coords = [int(float(x)) for x in row[1][1].strip().split(',')]

            ann.append(dict(
                is_crowd=0,
                category_id=1,
                bbox=[min(coords[0], coords[6]), min(coords[1], coords[3]),
                      max(coords[2], coords[4]) - min(coords[0], coords[6]),
                      max(coords[5], coords[7]) - min(coords[1], coords[3])],
                segmentation=[coords]))

        data["annotations"] = ann

        f_out.write(json.dumps(data))
        f_out.write("\n")

        if i % 1000 == 0:
            print(f'Processed: {i}/{total}')

    f_out.close()
    print("Done!")


if __name__ == '__main__':
    csv2txt()
