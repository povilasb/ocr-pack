from typing import Optional, Tuple

import click
import numpy as np

from .gfx import Image
from . import ml


@click.command()
@click.option('--resize-to', 'resize_to', type=str,
              help='Resize segments before saving to file. E.g. "8, 6" '
                   'where 8 is width and 6 is height.')
@click.option('--invert', 'invert_colors', type=bool, default=True,
              show_default=True,
              help='Invert colors before doing segmentation. Use the same '\
                   'value that was used fro training images.')
@click.option('--binary-threshold', '--bin-thr', 'binary_threshold',
              type=float,
              help='If this value is set, segment image will be transformed '\
                   'to have only two colors: background and foreground. '\
                   'Pixels with greater value than this will be obtain '\
                   'background color and with smaller value - foreground '\
                   'color. Use the same value that was used for training '\
                   'images.')
@click.option('-c', '--classifier', 'classifier_path', type=str,
              default='char_classifier.pkl',
              help='Absolute or relative path to character classifier.')
@click.argument('img_path')
def main(resize_to: Optional[str], invert_colors: bool,
         binary_threshold: Optional[float], classifier_path: str,
         img_path: str) -> None:
    img = Image.read_from(img_path, as_grey=True, background=1)
    if binary_threshold is not None:
        img = img.binary(binary_threshold)
    if invert_colors:
        img = img.invert()

    clf = ml.CharClassifier.load_from(classifier_path)

    transf = ImageTransformation(resize_to)
    char_arrays = [transform_segment(s, transf) for s in img.segments()]
    predicted_letters = clf.predict(char_arrays)
    print('Prediction:', predicted_letters)


class ImageTransformation:
    """Transformation parameters."""

    def __init__(self, resize_to: Optional[str]) -> None:
        self.resize_to = None

        new_size = None
        if resize_to is not None:
            new_size = [int(num) for num in resize_to.split(',')]
            self.resize_to = tuple(new_size)


def transform_segment(img: Image, transf: ImageTransformation) -> np.ndarray:
    if transf.resize_to is not None:
        img = img.resize_to(*transf.resize_to)
    return img.into_array().flatten()


if __name__ == '__main__':
    main()
