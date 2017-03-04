from typing import Tuple
import os

from skimage import io, filters, feature, segmentation, measure, morphology
import numpy as np

io.use_plugin('matplotlib')


# TODO:
#   extract character segments:
#       * http://www.cvc.uab.es/icdar2009/papers/3725a011.pdf
#   deskew segment images


# bbox: (y1, x1, y2, x2)


Rect = Tuple[int, int, int, int]


def extract_img(img: np.ndarray, rect: Rect) -> np.ndarray:
    return img[rect[0]:rect[2], rect[1]:rect[3]]


def binary_img(img: np.ndarray) -> np.ndarray:
    background_pos = img > 29
    char_pos = img < 30
    bin_img = img.copy()
    bin_img[char_pos] = 0
    bin_img[background_pos] = 255
    return bin_img


def img_segments(img: np.ndarray) -> list:
    labels = morphology.label(img, background=255)
    regions = measure.regionprops(labels)
    return sorted(regions, key=lambda r: r.bbox[1])


def new_char_file(chars_dir: str='chars') -> str:
    chars = os.listdir(chars_dir)
    return '{}/{}.png'.format(chars_dir, len(chars) or 0)


def fs_segment_image(img_file: str) -> None:
    img = io.imread(img_file)
    img = binary_img(img)
    for r in img_segments(img):
        io.imsave(new_char_file(), extract_img(img, r.bbox))


def main():
    imgs = os.listdir('images')
    for img in imgs:
        fs_segment_image('images/{}'.format(img))


main()
