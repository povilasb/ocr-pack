from typing import List

from sklearn.neighbors import KNeighborsClassifier
import numpy as np


class CharClassifier:
    def __init__(self, img_height: int, img_width: int):
        self.img_height = img_height
        self.img_width = img_width
        self._clf = KNeighborsClassifier(3)

    def fit(self, images: List[np.array], labels: List[str]) -> None:
        self._clf.fit(images, labels)

    def predict(self, img: List[np.array]) -> List[str]:
        return self._clf.predict(img)
