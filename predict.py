import sys

from sklearn.externals import joblib

from gfx import Image
from ml import CharClassifier


def do_ocr(img: Image, clf: CharClassifier) -> str:
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
    clf = joblib.load('char_classifier.pkl')
    print(do_ocr(img, clf))


if __name__ == '__main__':
    main()
