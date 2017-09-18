=====
About
=====

Trainer takes labelled images and creates the characters
`classifier <https://en.wikipedia.org/wiki/Statistical_classification>`_ which
is serialized with `Python pickles <https://docs.python.org/3/library/pickle.html>`_.

Currently only `k-nearest neighbors
<https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm>`_ classifier is
supported.

Command Line Interface
======================

::

    p3 -m ocrpack.trainer --help
    Usage: trainer.py [OPTIONS]

    Options:
    -i, --input-dir TEXT  Absolute or relative path to directory with labelled
                          character images.  [default: labelled-chars]
    -o, --output TEXT     Absolute or relative path to where character
                          classifier will be saved.  [default: char_classifier.pkl]
    --help                Show this message and exit.
