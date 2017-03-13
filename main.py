from typing import Tuple, Iterable, List
import os
import itertools as it

import numpy as np

from gfx import Image
import ml


# TODO:
#   extract character segments:
#       * http://www.cvc.uab.es/icdar2009/papers/3725a011.pdf
#       * match template of existing character to separate touching symbols
#       * use tesseract to recognize where segmentation fails
#   deskew segment images


# bbox: (y1, x1, y2, x2)


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
    imgs, labels = data.all_labelled_imgs()
    clf = ml.CharClassifier(data.max_height, data.max_width)
    clf.fit(imgs, labels)
    print(clf.predict(imgs[labels.index('H')]))

    # joblib.dump(clf, 'char_classifier.pkl')


main()
