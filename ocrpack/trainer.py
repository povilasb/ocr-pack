"""Trains character classifier.

Classifier is permanently stored to disk so that could be reloaded when
prediction operations are needed.
"""

import ml


def main():
    data = ml.TrainingData('labeller/labelled-chars')
    imgs, labels = data.all_labelled_imgs()

    clf = ml.CharClassifier(6, 8)
    clf.fit(imgs, labels)
    clf.save_to('char_classifier.pkl')


main()
