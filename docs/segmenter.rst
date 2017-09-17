=====
About
=====

Image segmantation is a process of dividing image into separate groups:

.. image:: img/char_segmentation.png

If you have text where characters are clearly separated, segmentation greatly
easens OCR task.

This tool does exactly that - segments an image.
To make image segmentation easier, there are some image preprocessing
capabilities:

* transform image to binary
* invert colors
* resize segments
* display intermediate results

Command Line Interface
======================

::

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
