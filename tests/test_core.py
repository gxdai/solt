import sys
import numpy as np
import cv2

from nose import with_setup

sys.path.insert(0,'..')
import fastaug.core as augs_core
import fastaug.transforms as trf

_globals = {'img': None, 'mask':None}

def img_2x2_generator():
    img = np.array([[1, 1],
                    [1, 1]]).reshape((2,2)).astype(np.uint8)
    for key in _globals:
        _globals[key] = None
    _globals['img'] = img

def img_mask_2x2_generator():
    img_2x2_generator() # generating image 2x2
    mask = np.array([[1, 0],
                     [0, 1]]).reshape((2,2)).astype(np.uint8) # Generating the mask
    _globals['mask'] = mask


def img_3x4_generator():
    for key in _globals:
        _globals[key] = None
    img = np.array([[1, 1, 1, 0],
                    [1, 0, 1, 1],
                    [1, 1, 1, 1]
                    ]).reshape((3, 4, 1)).astype(np.uint8)
    _globals['img'] = img

def img_mask_3x4_generator():
    img_3x4_generator()
    mask = np.array([[0, 1, 1, 1],
                    [0, 1, 1, 0],
                    [0, 1, 1, 0]
                    ]).reshape((3, 4, 1)).astype(np.uint8)
    _globals['mask'] = mask


@with_setup(img_2x2_generator)
def test_data_item_create_img():
    img = _globals['img']
    h, w = img.shape[0], img.shape[1]
    dc = augs_core.DataContainer((img,), 'I', h, w)
    assert len(dc) == 1
    assert np.array_equal(img, dc[0][0])
    assert dc[0][1] == 'I'

@with_setup(img_2x2_generator)
def test_pipeline_empty():
    img = _globals['img']
    h, w = img.shape[0], img.shape[1]
    dc = augs_core.DataContainer((img,), 'I', h, w)
    pipeline = augs_core.Pipeline()
    res, _ = pipeline(dc)[0]
    assert np.all(res == img)

@with_setup(img_2x2_generator)
def test_empty_pipeline_selective():
    img = _globals['img']
    h, w = img.shape[0], img.shape[1]
    dc = augs_core.DataContainer(img, 'I', h, w)
    pipeline = augs_core.SelectivePipeline()
    res, _ = pipeline(dc)[0]
    assert np.all(res == img)

@with_setup(img_mask_3x4_generator)
def test_img_mask_horizontal_flip():
    img, mask = _globals['img'], _globals['mask']
    h, w = img.shape[0], img.shape[1]
    dc = augs_core.DataContainer((img, mask), 'IM', h, w)

    pipeline = augs_core.Pipeline([
        trf.RandomFlip(p=1)
    ])

    dc = pipeline(dc)
    img_res, _ = dc[0]
    mask_res, _ = dc[1]

    assert np.array_equal(cv2.flip(img, 0), img_res)
    assert np.array_equal(cv2.flip(mask, 0), mask_res)

@with_setup(img_mask_3x4_generator)
def test_img_mask_mask_horizontal_flip():
    img, mask = _globals['img'], _globals['mask']
    h, w = img.shape[0], img.shape[1]
    dc = augs_core.DataContainer((img, mask, mask), 'IMM', h, w)

    pipeline = augs_core.Pipeline([
        trf.RandomFlip(p=1, axis=0)
    ])

    dc = pipeline(dc)
    img_res, _ = dc[0]
    mask_res, _ = dc[1]

    assert np.array_equal(cv2.flip(img, 0), img_res)
    assert np.array_equal(cv2.flip(mask, 0), mask_res)


@with_setup(img_mask_3x4_generator)
def test_img_mask_vertical_flip():
    img, mask = _globals['img'], _globals['mask']
    h, w = img.shape[0], img.shape[1]
    dc = augs_core.DataContainer((img, mask), 'IM', h, w)

    pipeline = augs_core.Pipeline([
        trf.RandomFlip(p=1, axis=1)
    ])

    dc = pipeline(dc)
    img_res, _ = dc[0]
    mask_res, _ = dc[1]

    assert np.array_equal(cv2.flip(img, 1), img_res)
    assert np.array_equal(cv2.flip(mask, 1), mask_res)