.. Fully Agnostic Atomic Render Environment documentation master file, created by
   sphinx-quickstart on Mon Dec 25 21:11:06 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Fully Agnostic Atomic Render Environment's documentation!
====================================================================

Core philosophy
---------------

The purpose of :program:`FAARE` is to efficiently leverage `Blender <https://www.blender.org/>`_ 
to produce high-quality renders of your atomic systems. It does this by providing
a very large set default settings which be easily extended or replaced by minimum
user effort. :program:`FAARE` can be executed natively, in a Linux WSL or remotely.
Under the hood, it uses a combination of Python scripts and `json <https://www.json.org/json-en.html>`_ type
template files to produce a single :code:`manifest.json` file. This file
is read in Blender to produce a single render image.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
