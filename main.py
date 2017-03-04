from typing import Tuple
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


def main():
    img = io.imread('images/HXUUNR.jpg')
    img = binary_img(img)

    labels = morphology.label(img, background=255)
    regions = measure.regionprops(labels)
    regions = sorted(regions, key=lambda r: r.bbox[1])

    io.imsave('result.png', extract_img(img, regions[1].bbox))

    for r in regions:
        io.imshow(extract_img(img, r.bbox))
        io.show()


main()
