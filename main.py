from typing import Tuple, Iterable, List
import os
import itertools as it

from skimage import io, filters, feature, segmentation, measure, morphology
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

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
    def __init__(self, array: np.ndarray, label: str='',
                 background: int=255) -> None:
        self._array = array
        self._background = background

        self.label = label
        self.height = array.shape[0]
        self.width = array.shape[1]

    @classmethod
    def read_from(cls: 'Image', fname: str, background=255) -> 'Image':
        img = io.imread(fname)
        return cls(img, background=background)

    @classmethod
    def read_from_array(cls: 'Image', fname: str, background=1) -> 'Image':
        return cls(np.load(fname), background=background)

    def with_label(self, label: str) -> 'Image':
        self.label = label
        return self

    def with_background(self, background: int) -> 'Image':
        new_img = self._array.copy()
        new_img[new_img == self._background] = background
        return Image(new_img, self.label, background)

    def save_to(self, fname: str) -> None:
        np.save(fname, self._array, allow_pickle=False)

    def binary(self, threshold: int=30) -> 'Image':
        background_pos = self._array >= threshold
        char_pos = self._array < threshold
        bin_img = self._array.copy()
        bin_img[char_pos] = 0
        bin_img[background_pos] = self._background
        return Image(bin_img, self.label)

    def invert(self) -> 'Image':
        """Only works with binary images."""
        background_pos = self._array == self._background
        foreground_pos = self._array == 0
        new_img = self._array.copy()
        new_img[foreground_pos] = self._background
        new_img[background_pos] = 0
        return Image(new_img, self.label)

    def rect(self, rect: Rect) -> 'Image':
        return Image(self._array[rect[0]:rect[2], rect[1]:rect[3]])

    def segments(self) -> Iterable['Image']:
        labels = morphology.label(self._array, background=self._background)
        regions = measure.regionprops(labels)
        return map(lambda region: self.rect(region.bbox),
                   sorted(regions, key=lambda r: r.bbox[1]))

    def extend_to(self, new_height: int, new_width: int) -> 'Image':
        height, width = self._array.shape
        return Image(np.pad(
            self._array,
            ((0, new_height - height), (0, new_width - width)),
            mode='constant', constant_values=self._background
        ), self.label, background=self._background)

    def show(self) -> None:
        io.imshow(self._array)
        io.show()


def images_in(dir_path: str) -> Iterable[Image]:
    return map(lambda fname: Image.read_from_array('{}/{}'.format(dir_path,
                                                                  fname)),
               os.listdir(dir_path))


def labelled_images_in(dir_path: str, label: str) -> Iterable[Image]:
    return map(lambda img: img.with_label(label), images_in(dir_path))


def new_char_file(chars_dir: str='chars') -> str:
    chars = os.listdir(chars_dir)
    return '{}/{}.npy'.format(chars_dir, len(chars) or 0)


def fs_segment_image(img: Image) -> None:
    for segment in img.binary().segments():
        segment.save_to(new_char_file())


def segment_all_captchas() -> None:
    for img in images_in('images'):
        fs_segment_image(img)


def max_char_size_in(imgs: Iterable[Image]) -> Tuple[int, int]:
    imgs1, imgs2 = it.tee(imgs)
    return (
        max(map(lambda i: i.height, imgs1)),
        max(map(lambda i: i.width, imgs2)),
    )


def all_labelled_images() -> Iterable[Image]:
    return it.chain.from_iterable([
        images_in('labelled-chars/{}'.format(char))
        for char in os.listdir('labelled-chars')
    ])


class TrainingData:
    def __init__(self) -> None:
        self.max_height, self.max_width = max_char_size_in(
            all_labelled_images())

    def all_labelled_imgs(self) -> Tuple[List[np.ndarray], List[str]]:
        imgs = []
        labels = []
        for char in os.listdir('labelled-chars'):
            i, l = self.imgs_with_labels(char)
            imgs += i
            labels += l
        return imgs, labels

    def imgs_with_labels(self, char: str) -> Tuple[List[np.ndarray], List[str]]:
        imgs = list(self.arrays_for(char))
        return imgs, list(char * len(imgs))

    def arrays_for(self, char: str) -> Iterable[np.ndarray]:
        return map(lambda img: img._array.flatten(), self.imgs_for(char))

    def imgs_for(self, char: str) -> Iterable[Image]:
        return map(lambda img: img.extend_to(self.max_height, self.max_width)
                   .invert(),
                   labelled_images_in('labelled-chars/{}'.format(char), char))


def main():
    data = TrainingData()
    print('Normalized size:', data.max_height, data.max_width)

    imgs, labels = data.all_labelled_imgs()
    clf = KNeighborsClassifier(3)
    clf.fit(imgs, labels)
    print(clf.predict(imgs[labels.index('H')]))

    chars = list(Image.read_from('images.bk/GYNFEE.jpg').binary().segments())
    for char in chars:
        char = char.with_background(1)\
            .extend_to(data.max_height, data.max_width)\
            .invert()._array.flatten()
        print(clf.predict(char))


main()
