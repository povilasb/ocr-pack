from typing import Optional
import os

import click

import sys
sys.path.insert(0, '..')
import gfx


# TODO:
#   extract character segments:
#       * http://www.cvc.uab.es/icdar2009/papers/3725a011.pdf
#       * match template of existing character to separate touching symbols
#       * use tesseract to recognize where segmentation fails
#   deskew segment images
# TODO: option to save segments as NumPy arrays?

@click.command()
@click.option('--file', '-f', 'fname', type=str, required=True,
              help='Absolute or relative path to image.',)
@click.option('--invert', 'invert_colors', type=bool, default=True,
              show_default=True,
              help='Invert colors before doing segmentation. This option'
                   'also makes the stored segments to be inverted.')
@click.option('--resize-to', 'resize_to', type=str,
              help='Resize segments before saving to file. E.g. "8, 6" '
                   'where 8 is width and 6 is height.')
@click.option('--show', 'show_img', default=False, flag_value='show',
              help='Show image after transformations before segmentation.'
                   'Useful for debugging.')
@click.option('--show-only', 'show_img_only', default=False,
              flag_value='show-only',
              help='Only show image after transformations before segmentation.'
                   'But do not proceed with segmentation.')
@click.option('--binary-threshold', '--bin-thr', 'binary_threshold',
              type=float,
              help='If this value is set, resulting image will have only two '\
                    'colors: background and foreground. Pixels with greater '\
                    'value than this will be obtain background color and '\
                    'with smaller value - foreground color.')
@click.option('--out-dir', '-o', 'save_to_dir', type=str,
              help='Store image segments in this directory. Every segment '\
                   'is stored as a separate PNG image whose name is sequence '\
                   'number in the directory. E.g. 1.png, 2.png, 3.png, etc. '\
                   'If this option is not specified, segments are simply '\
                   'displayed.')
def main(fname: str, invert_colors: bool, resize_to: str, show_img: bool,
         show_img_only: bool, binary_threshold: Optional[float],
         save_to_dir: Optional[str],) -> None:
    img = gfx.Image.read_from(fname, as_grey=True, background=1)

    if binary_threshold is not None:
        img = img.binary(binary_threshold)
    if invert_colors:
        img = img.invert()

    if show_img or show_img_only:
        img.show()
    if show_img_only:
        return

    new_size = None
    if resize_to is not None:
        new_size = [int(num) for num in resize_to.split(',')]
    for s in img.segments():
        if new_size is not None:
            s = s.resize_to(new_size[0], new_size[1])
        if save_to_dir is None:
            s.show()
        else:
            s.save_to(next_file(save_to_dir))


# TODO: duplicate with ../labeller/fs.py
def next_file(in_dir: str) -> str:
    files = os.listdir(in_dir)
    return '{}/{}.png'.format(in_dir, len(files) or 0)


if __name__ == '__main__':
    main()
