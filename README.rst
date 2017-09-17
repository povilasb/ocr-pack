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
* `image segmentation tool <docs/segmenter.rst>`_
* image labelling Web based app
* machine learning classifier and a CLI tool to build it
* OCR tool to predict characters in a given image

Labeller
========

This is `Flask <http://flask.pocoo.org/>`_ based Web application that
helps to label image samples as characters.
Then those character images might be used to train the classifier.

See Also
========

* https://matthewearl.github.io/2016/05/06/cnn-anpr/
