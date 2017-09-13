from typing import Iterable, Tuple, List

import numpy as np
from skimage import io, morphology, measure
io.use_plugin('matplotlib')


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
    def read_from(cls: 'Image', fname: str, as_grey: bool=False,
                  background=255) -> 'Image':
        img = io.imread(fname, as_grey=as_grey)
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
        io.imsave(fname, self._array)

    def save_array_to(self, fname: str) -> None:
        """Stores underlying NumPy array to file."""
        np.save(fname, self._array, allow_pickle=False)

    def binary(self, threshold: int=30) -> 'Image':
        background_pos = self._array >= threshold
        char_pos = self._array < threshold
        bin_img = self._array.copy()
        # TODO: 0 is not the best value to mark object - background might also
        # be 0.
        bin_img[char_pos] = 0
        bin_img[background_pos] = self._background
        return Image(bin_img, self.label, self._background)

    def invert(self) -> 'Image':
        """Only works with binary images."""
        background_pos = self._array == self._background
        foreground_pos = self._array == 0
        new_img = self._array.copy()
        new_img[foreground_pos] = self._background
        new_img[background_pos] = 0
        return Image(new_img, self.label, background=0)

    def rect(self, rect: Rect) -> 'Image':
        return Image(self._array[rect[0]:rect[2], rect[1]:rect[3]],
                     self.label, background=self._background)

    def segments(self) -> List['Image']:
        labels = morphology.label(self._array, background=self._background)
        regions = measure.regionprops(labels)
        return [self.rect(region.bbox) for region in
                sorted(regions, key=lambda r: r.bbox[1])]

    def resize_to(self, new_height: int, new_width: int) -> 'Image':
        height, width = self._array.shape
        if height < new_height:
            height = new_height
        if width < new_width:
            width = new_width
        new_img = self.extend_to(height, width)
        return new_img.rect((0, 0, new_height, new_width))

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
