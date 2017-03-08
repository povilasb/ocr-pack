from typing import Tuple, Iterable
import os
import itertools as it

from skimage import io, filters, feature, segmentation, measure, morphology
import numpy as np

io.use_plugin('matplotlib')


# TODO:
#   extract character segments:
#       * http://www.cvc.uab.es/icdar2009/papers/3725a011.pdf
#       * match template of existing character to separate touching symbols
#       * use tesseract to recognize where segmentation fails
#   deskew segment images


# bbox: (y1, x1, y2, x2)


Rect = Tuple[int, int, int, int]


class Image:
    def __init__(self, array: np.ndarray) -> None:
        self._array = array
        self.height = array.shape[0]
        self.width = array.shape[1]

    @classmethod
    def read_from(cls: 'Image', fname: str) -> 'Image':
        return cls(io.imread(fname))

    def save_to(self, fname: str) -> None:
        io.imsave(fname, self._array)

    def binary(self) -> 'Image':
        background_pos = self._array > 29
        char_pos = self._array < 30
        bin_img = self._array.copy()
        bin_img[char_pos] = 0
        bin_img[background_pos] = 255
        return Image(bin_img)

    def rect(self, rect: Rect) -> 'Image':
        return Image(self._array[rect[0]:rect[2], rect[1]:rect[3]])

    def segments(self) -> Iterable['Image']:
        labels = morphology.label(self._array, background=255)
        regions = measure.regionprops(labels)
        return map(lambda region: self.rect(region.bbox),
                   sorted(regions, key=lambda r: r.bbox[1]))

    def extend_to(self, new_height: int, new_width: int) -> 'Image':
        height, width = self._array.shape
        return Image(np.pad(
            self._array,
            ((0, new_height - height), (0, new_width - width)),
            mode='constant', constant_values=255
        ))

    def show(self) -> None:
        io.imshow(self._array)
        io.show()


def images_in(dir_path: str) -> Iterable[Image]:
    return map(lambda fname: Image.read_from('{}/{}'.format(dir_path, fname)),
               os.listdir(dir_path))


def new_char_file(chars_dir: str='chars') -> str:
    chars = os.listdir(chars_dir)
    return '{}/{}.png'.format(chars_dir, len(chars) or 0)


def fs_segment_image(img: Image) -> None:
    for segment in img.binary().segments():
        segment.save_to(new_char_file())


def segment_all_captchas() -> None:
    for img in images_in('images'):
        fs_segment_image(img)


def max_char_size(img: Image) -> Tuple[int, int]:
    chars1, chars2 = it.tee(img.segments())
    max_height = max(map(lambda c: c.height, chars1))
    max_width = max(map(lambda c: c.width, chars2))
    return max_height, max_width


def max_char_size_in_images() -> Tuple[int, int]:
    max_height = 0
    max_width = 0
    for img in images_in('images'):
        height, width = max_char_size(img)
        max_height = max(max_height, height)
        max_width = max(max_width, width)
    return max_height, max_width


def main():
    max_height, max_width = max_char_size_in_images()
    print(max_height, max_width)


main()
