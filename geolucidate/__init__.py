"""
:mod:`geolucidate` is a Python module for identifying and parsing
geographic coordinates in text.  For most purposes, calling
:func:`~.replace` with the text to be processed will suffice.


>>> from geolucidate import replace
>>> replace("58147N/07720W")
u'<a href="http://maps.google.com/maps?q=58.235278%2C-77.333333+%2858147N%2F07720W%29&ll=58.235278%2C-77.333333&t=h" title="58147N/07720W (58.235278, -77.333333)">58147N/07720W</a>'

"""

from functions import replace, google_maps_link
