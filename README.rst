=====
About
=====

OCR pack contains multiple tools and Python libraries to make optical
character recognition easer.
Currently this solution is only viable when characters are clearly segmented,
meaning they don't touch.
I know this doesn't cover many OCR cases, but at the same time it can solve
some custom problems too:

* text recognition in desktop window
* license plate recognition
* simple `CAPTCHA <https://en.wikipedia.org/wiki/CAPTCHA>`_ recognition

This solution overall is the similar to `MNIST
<http://blog.povilasb.com/posts/mnist-with-scikit-learn/>`_ solution where
the algorithm can only recognize single digit.
The only difference is that this solution works with any characters.

The pack includes:

* image manipulation library for Python 3
* image segmentation tool
* image labelling Web based app
* machine learning classifier and a CLI tool to build it
* OCR tool to predict characters in a given image

Segmenter
=========

It is a small CLI tool to segment image into characters.

Usage::

    python3 -m ocrpack.segmenter --help
    Usage: main.py [OPTIONS]

    Options:
      -f, --file TEXT                 Absolute or relative path to image.
                                      [required]
      --invert BOOLEAN                Invert colors before doing segmentation.
                                      This option also makes the stored segments to
                                      be inverted.  [default: True]
      --resize-to TEXT                Resize segments before saving to file. E.g.
                                      "8, 6" where 8 is width and 6 is height.
      --show                          Show image after transformations before
                                      segmentation.Useful for debugging.
      --show-only                     Only show image after transformations before
                                      segmentation.But do not proceed with
                                      segmentation.
      --binary-threshold, --bin-thr FLOAT
                                      If this value is set, resulting image will
                                      have only two colors: background and
                                      foreground. Pixels with greatervalue than
                                      this will be obtain background color and
                                      with smaller value - foreground color.
      -o, --out-dir TEXT              Store image segments in this directory.
                                      Every segment is stored as a separate PNG
                                      image whose name is sequence number in the
                                      directory. E.g. 1.png, 2.png, 3.png, etc. If
                                      this option is not specified, segments are
                                      simply displayed.
      --help                          Show this message and exit.

Labeller
========

This is `Flask <http://flask.pocoo.org/>`_ based Web application that
helps to label image samples as characters.
Then those character images might be used to train the classifier.

See Also
========

* https://matthewearl.github.io/2016/05/06/cnn-anpr/
