# Convert to format supported by MMOCR

import xml.etree.ElementTree as ET
import json
import os
import argparse

char_set = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def parse_args():
    parser = argparse.ArgumentParser('Convert annotation files from XML to TXT')
    parser.add_argument('input', type=str, help='XML folder path')
    parser.add_argument('output', type=str, help='Output folder path')
    parser.add_argument('ignore_latin', type=str, default="false", help='Ignore latin (English) words')
    args = parser.parse_args()

    return args


def xml2txt():
    args = parse_args()

    print('Starting...')

    f_out = open(os.path.join(args.output, 'gt_mmocr.txt'), 'w')

    files = []
    for filename in os.listdir(args.input):
        if filename.endswith(".xml"):
            files.append(filename)

    total = len(files)

    for i, filename in enumerate(files):
        f_in = open(os.path.join(args.input, filename), 'r', encoding='utf8')

        tree = ET.parse(f_in)
        root = tree.getroot()

        f_in.close()

        data = dict()
        ann = []

        # Adds file_name to our txt object
        for path in root.iter('path'):
            data['file_name'] = path.text

        # Adds height, width to our txt object
        for size in root.iter('size'):
            for dim in size:

                if dim.tag == 'height':
                    data['height'] = dim.text

                if dim.tag == 'width':
                    data['width'] = dim.text

        # Adds bounding box and segmentation info to our txt object
        for segmentation in root.iter("object"):

            latin_word = False
            label = ''

            for key in segmentation:

                if key.tag == 'name':
                    for char in key.text.lower():
                        if char in char_set and args.ignore_latin.lower() == 'true':
                            latin_word = True
                            break

                    if latin_word:
                        break
                    else:
                        label = key.text

                if key.tag == 'bndbox':
                    for coord in key:

                        if coord.tag == 'xmin':
                            xmin = int(coord.text)

                        if coord.tag == 'ymin':
                            ymin = int(coord.text)

                        if coord.tag == 'xmax':
                            xmax = int(coord.text)

                        if coord.tag == 'ymax':
                            ymax = int(coord.text)

            if not latin_word:
                ann.append(dict(
                    is_crowd=0,
                    category_id=1,
                    bbox=[xmin, ymin, xmax - xmin, ymax - ymin],
                    segmentation=[[xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax]]))
            else:
                print(f'Skipping {key.text}')

        data["annotations"] = ann

        if len(ann) > 0:
            f_out.write(json.dumps(data))
            f_out.write("\n")

        print(f'Processed: {i + 1}/{total}')

    f_out.close()
    print("Done!")


if __name__ == '__main__':
    xml2txt()
