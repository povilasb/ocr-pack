"""Trains character classifier.

Classifier is permanently stored to disk so that could be reloaded when
prediction operations are needed.
"""

import click

from . import ml


@click.command()
@click.option('-i', '--input-dir', 'input_dir', type=str,
              default='labelled-chars',
              help='Absolute or relative path to directory with labelled '\
                   'character images.',)
@click.option('-o', '--output', 'classifier_path', type=str,
              default='char_classifier.pkl',
              help='Absolute or relative path to where character classifier '\
                   'will be saved.',)
def main(input_dir: str, classifier_path: str) -> None:
    data = ml.TrainingData(input_dir)
    imgs, labels = data.all_labelled_imgs()

    clf = ml.CharClassifier(0, 0)
    clf.fit(imgs, labels)
    clf.save_to(classifier_path)


main()
