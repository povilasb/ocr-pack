=====
About
=====

Extractor is a tool that does optical character recognition in a given image.
Basically it

1. loads given image
2. preprocesses it the same way it was processed during segmentation
3. segments the characters
4. loads trained classifier
5. predicts the label of every character
6. prints result

For example,

.. image:: img/grayscale.png

::

    $ p3 -m ocrpack.extractor --invert true --resize-to 8,12 --bin-thr 0.39 -c char_classifier.pkl num.png
    Prediction: ['4' '3' '1']

Command Line Interface
======================

::

    p3 -m ocrpack.extractor --help
    Usage: extractor.py [OPTIONS] IMG_PATH

    Options:
      --resize-to TEXT                Resize segments before saving to file. E.g.
                                      "8, 6" where 8 is width and 6 is height.
      --invert BOOLEAN                Invert colors before doing segmentation. Use
                                      the same value that was used fro training
                                      images.  [default: True]
      --binary-threshold, --bin-thr FLOAT
                                      If this value is set, segment image will be
                                      transformed to have only two colors:
                                      background and foreground. Pixels with
                                      greater value than this will be obtain
                                      background color and with smaller value -
                                      foreground color. Use the same value that
                                      was used for training images.
      -c, --classifier TEXT           Absolute or relative path to character
                                      classifier.
      --help                          Show this message and exit.

Command line parameters are very similar to ones in `segmenter <segmenter.rst>`_.
