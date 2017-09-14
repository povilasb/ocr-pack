import os
from typing import List, Iterable, Tuple

from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib
import numpy as np

from gfx import Image


class CharClassifier:
    def __init__(self, img_height: int, img_width: int) -> None:
        self.img_height = img_height
        self.img_width = img_width
        self._clf = KNeighborsClassifier(3)

    def fit(self, images: List[np.array], labels: List[str]) -> None:
        self._clf.fit(images, labels)

    def predict(self, img: List[np.array]) -> List[str]:
        return self._clf.predict(img)

    def save_to(self, fname: str) -> None:
        joblib.dump(self, fname)

    @classmethod
    def load_from(cls: 'CharClassifier', fname: str) -> 'CharClassifier':
        return joblib.load(fname)


class TrainingData:
    """Prepares training data for CharClassifier.

    Reads segmented labelled character images from disk.
    """

    def __init__(self, labelled_imgs_dir: str) -> None:
        """
        Args:
            labelled_imgs_dir: directory where labelled images are stored.
                Expected directory structure is:
                    ./labelled-dir
                    |__ 7
                    |  |__ 0.png
                    |  |__ 1.png
                    |__ A
                    |  |__ 0.png
                    |  |__ 1.png
        """
        self._imgs_dir = labelled_imgs_dir

    def all_labelled_imgs(self) -> Tuple[List[np.ndarray], List[str]]:
        """Reads all images with their labels.

        Image data and labels are returned in separated lists.
        Both returned lists have the same size.
        labels[i] refers to images[i].

        Result is suitable for CharClassifier.fit() method.
        """
        imgs = []
        labels = []
        for label in os.listdir(self._imgs_dir):
            i, l = self.arrays_with_labels_for(label)
            imgs += i
            labels += l
        return imgs, labels

    def arrays_with_labels_for(
            self, label: str) -> Tuple[List[np.ndarray], List[str]]:
        """Returns labels together with image arrays.

        Similar to self.arrays_for() but also returns another list which
        holds label per image data array.
        """
        imgs = list(self.arrays_for(label))
        return imgs, list([label] * len(imgs))

    def arrays_for(self, label: str) -> Iterable[np.ndarray]:
        """Reads label images and returns in flattened array format.

        Similar to self.imgs_for() but instead of returning images, it returns
        flattened image data arrays.
        """
        return map(
            lambda img: img.into_array().flatten(),
            self.imgs_for(label)
        )

    def imgs_for(self, label: str) -> Iterable[Image]:
        """Reads all images for specified label."""
        dir_for_label = '{}/{}'.format(self._imgs_dir, label)
        return map(
            lambda fname: Image.read_from(
                '{}/{}'.format(dir_for_label, fname)),
            os.listdir(dir_for_label)
        )
