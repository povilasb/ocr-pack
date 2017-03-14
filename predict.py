import sys

from gfx import Image
import ml


def do_ocr(img: Image, clf: ml.CharClassifier) -> str:
    chars = img.binary().segments()
    char_arrays = map(
        lambda c: c.with_background(1)
                   .extend_to(clf.img_height, clf.img_width)
                   .invert()._array.flatten(),
        chars
    )
    predicted_letters = clf.predict(list(char_arrays))
    return ''.join(predicted_letters)


def main(args=sys.argv[1:]):
    img_path = args[0]
    img = Image.read_from(img_path)
    clf = ml.CharClassifier.load_from('char_classifier.pkl')
    print(do_ocr(img, clf))


if __name__ == '__main__':
    main()
