.. rst syntax: https://deusyss.developpez.com/tutoriels/Python/SphinxDoc/
.. version conv: https://peps.python.org/pep-0440/
.. icons: https://specifications.freedesktop.org/icon-naming-spec/latest/ar01s04.html or https://www.pythonguis.com/faq/built-in-qicons-pyqt/
.. pyqtdoc: https://www.riverbankcomputing.com/static/Docs/PyQt6/
.. colors-spaces: https://trac.ffmpeg.org/wiki/colorspace

.. image:: https://img.shields.io/badge/License-MIT-green.svg
    :alt: [license MIT]
    :target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/badge/linting-pylint-green
    :alt: [linting: pylint]
    :target: https://github.com/pylint-dev/pylint

.. image:: https://img.shields.io/badge/tests-pass-green
    :alt: [testing]
    :target: https://docs.pytest.org/

.. image:: https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue
    :alt: [versions]
    :target: https://framagit.org/robinechuca/cutcutcodec/-/blob/main/run_tests.sh

.. image:: https://static.pepy.tech/badge/cutcutcodec
    :alt: [downloads]
    :target: https://www.pepy.tech/projects/cutcutcodec

.. image:: https://readthedocs.org/projects/cutcutcodec/badge/?version=latest
    :alt: [documentation]
    :target: https://cutcutcodec.readthedocs.io/latest/

Useful links:
`Binary Installers <https://pypi.org/project/cutcutcodec>`_ |
`Source Repository <https://framagit.org/robinechuca/cutcutcodec>`_ |
`Online Documentation <https://cutcutcodec.readthedocs.io>`_ |


Description
===========

This **video editing software** has been designed for speed and to implement some effects that are hard to find elsewhere.
The kernel is written in python and C, so it's easy to integrate it in your own project (module ``cutcutcodec.core``).
Although it allows you to fine-tune many parameters, it's smart enough to find the settings that are best suited to your project.

This software is **light**, **fast** and **highly configurable** for the following reasons:

#. Based on ffmpeg, this software supports an incredible number of formats and codecs.
#. This software allows editing the assembly graph. Compared to a timeline, this representation permits to do everything.
#. This software doesn't export the final video directly from the graphic interface. Instead, it generates a python script. You can edit this script yourself, giving you infinite possibilities!
#. A complete test benchmark guarantees an excelent kernel reliability.
#. Powered by `torch <https://pytorch.org/>`_ and written in C, this software efficiently exploits the CPU and GPU in order to make it very fast.
#. Video export is performed without a graphical interface, releasing a large part of computer resources to speed up export.
#. This software is able to optimize the assembly graph in order to limit calculation waste.
#. The code is parallelised to take advantage of all the CPU threads, making it extremely fast.


Features
========

Audio
-----

* General properties
    #. Supports a large number of channels (mono, stereo, 5.1, 7.1, ...) with all sampeling rate.
    #. Automatic detection of the optimal sample frequency.
* Generation
    #. White-noise generation.
    #. Generate any audio signal from any equation.
* Filters
    #. Cutting, translate and concatenate.
    #. Add multiple tracks.
    #. Arbitrary equation on several channels of several tracks. (dynamic volume, mixing, wouawoua, ...)
    #. Finite Impulse Response (FIR) invariant filter. (reverb, equalizer, echo, delay, volume, ...)
    #. Denoising based on Winer filtering.
    #. Hight quality anti aliasing low pass filter (based on FIR).

Video
-----

* General properties
    #. Unlimited support of all image resolutions. (FULL HD, 4K, 8K, ...)
    #. No limit on fps. (60fps, 120fps, ...)
    #. Automatic detection of the optimal resolution and fps.
    #. Support for the alpha transparency layer.
    #. Floating-point image calculation for greater accuracy.
* Generation
    #. White-noise generation.
    #. Generate any video signal from any equation.
    #. Mandelbrot fractal generation.
* Filters
    #. Cutting, translate and concatenate.
    #. Resize and crop (high quality, no aliasing).
    #. Overlaying video tracks (with transparency control).
    #. Apply an arbitrary equation one several video streams.
