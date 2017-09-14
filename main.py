from typing import Tuple, Iterable, List
import os
import itertools as it

import numpy as np

from gfx import Image
import ml


# bbox: (y1, x1, y2, x2)


def images_in(dir_path: str) -> Iterable[Image]:
    return map(lambda fname: Image.read_from_array('{}/{}'.format(dir_path,
                                                                  fname)),
               os.listdir(dir_path))


def labelled_images_in(dir_path: str, label: str) -> Iterable[Image]:
    return map(lambda img: img.with_label(label), images_in(dir_path))


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


# TODO: remove once ml.TrainingData is done.
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
    imgs, labels = data.all_labelled_imgs()
    clf = ml.CharClassifier(data.max_height, data.max_width)
    clf.fit(imgs, labels)
    print(clf.predict(imgs[labels.index('H')]))


main()
