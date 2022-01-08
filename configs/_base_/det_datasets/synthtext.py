root = 'data/synthtext'

# dataset with type='TextDetDataset'
train = dict(
    type='TextDetDataset',
    img_prefix=f'{root}/imgs',
    ann_file=f'{root}/instances_test.txt',
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
    img_prefix=f'{root}/imgs',
    ann_file=f'{root}/instances_test.txt',
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
