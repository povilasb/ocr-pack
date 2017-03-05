from typing import Tuple, Iterable
import os
import itertools as it

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


def img_segments(img: np.ndarray) -> Iterable[np.ndarray]:
    labels = morphology.label(img, background=255)
    regions = measure.regionprops(labels)
    return map(lambda region: extract_img(img, region.bbox),
               sorted(regions, key=lambda r: r.bbox[1]))


def new_char_file(chars_dir: str='chars') -> str:
    chars = os.listdir(chars_dir)
    return '{}/{}.png'.format(chars_dir, len(chars) or 0)


def fs_segment_image(img_file: str) -> None:
    img = io.imread(img_file)
    img = binary_img(img)
    for segment in img_segments(img):
        io.imsave(new_char_file(), segment)


def segment_all_captchas() -> None:
    imgs = os.listdir('images')
    for img in imgs:
        fs_segment_image('images/{}'.format(img))


def extend_img(img: np.ndarray, new_height: int, new_width: int) -> np.ndarray:
    height, width = img.shape
    return np.pad(
        img,
        ((0, new_height - height), (0, new_width - width)),
        mode='constant', constant_values=255
    )


def main():
    img = io.imread('images/GYNFEE.jpg')
    chars1, chars2, chars3 = it.tee(img_segments(binary_img(img)), 3)
    max_height = max(map(lambda c: c.shape[0], chars1))
    max_width = max(map(lambda c: c.shape[1], chars2))
    for char_img in chars3:
        io.imshow(extend_img(char_img, max_height, max_width))
        io.show()


main()
