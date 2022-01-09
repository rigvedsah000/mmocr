root = '/home/ocr/datasets/synthText/detection-dataset/telugu'

# dataset with type='TextDetDataset'
train = dict(
    type='TextDetDataset',
    img_prefix=f'{root}/output',
    ann_file=f'{root}/gt_mmocr_train.txt',
    loader=dict(
        type='HardDiskLoader',
        repeat=4,
        parser=dict(
            type='LineJsonParser',
            keys=['file_name', 'height', 'width', 'annotations'])),
    pipeline=None,
    test_mode=False)

test = dict(
    type='TextDetDataset',
    img_prefix=f'{root}/output',
    ann_file=f'{root}/gt_mmocr_val.txt',
    loader=dict(
        type='HardDiskLoader',
        repeat=1,
        parser=dict(
            type='LineJsonParser',
            keys=['file_name', 'height', 'width', 'annotations'])),
    pipeline=None,
    test_mode=True)

train_list = [train]

test_list = [test]
