from typing import List

from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib
import numpy as np


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
