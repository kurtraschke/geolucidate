.. geolucidate documentation master file, created by
   sphinx-quickstart on Wed Jan 26 00:31:05 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to geolucidate's documentation!
=======================================

:mod:`geolucidate` is a Python module for identifying and parsing
geographic coordinates in text.  By default, :mod:`geolucidate` will
replace detected coordinates with an HTML link to an online map, but
the parser can also be used to annotate coordinates with machine-readable
metadata or perform similar tasks.

The regular expression used for parsing (contained in
:mod:`geolucidate.parser`) accepts roughly fifteen different formats
of degrees, minutes, and seconds, or degrees and minutes with a
decimal fraction, with varying punctuation delimiting the components.
These formats range from (for example) "49º41’34″N 093º37’54″W" to
"6828N/8234W".  Regardless of input format, the output is formatted as
decimal degrees.

Contents:

.. toctree::
   :maxdepth: 3

   doc
   input

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

