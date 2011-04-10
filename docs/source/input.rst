Notes on input formats
======================

:mod:`geolucidate` accepts a wide range of inputs containing degrees,
minutes, and seconds or a decimal fraction of minutes.  Degrees and
seconds are optional; the precision of the output will be adjusted
automatically if they are not present.  However, the latitude and
longitude must be of equal precision.  Additionally, latitude and
longitude must both be present, and in that order.

Additionally, the following conditions are placed on input:

* The input is case-insensitive.

* The latitude direction may come before or after the latitude, and
  must be one of "NORTH", "SOUTH", "N", or "S".

* The longitude direction may come before or after the longitude, and
  must be one of "EAST", "WEST", "E", or "W".

* Latitude and longitude directions must be in the same position: they
  can either precede or follow the values, but must not be mixed.

* A separator is not required between the latitude and longitude, but
  if present, it must be a space, forward slash, or comma.  If a
  separator is present, a space may optionally be present before and
  after the separator.

* Degree values may be followed by a space or a degree mark, which
  must be one of the following values: 
  ``º``, ``°``, ``.``, ``-``, ``DEGREES,``.

* Minute values may be followed by a space or one of the following
  optional punctuation marks:
  ``'``, ``"``, ``.``, ``MINUTES,``.

* Second values may be followed by one of the following optional
  punctuation marks:
  ``"``, ``'``, ``SECONDS``.

* 'Seconds' which are preceded by a decimal point or which are greater
  than 59 will be treated as a decimal fraction of minutes; that is,
  they will be divided by 100 rather than 60.

* Degree marks and punctuation following minutes and seconds are only
  accepted if a degree mark is present following the latitude
  degrees.  The effect of this is that the use of degree
  marks/punctuation must be consistent.

* Numeric values must be within sensible ranges; degrees greater than
  90 for latitude or 180 for longitude are not accepted; nor are minutes
  or seconds (subject to the caveat above regarding decimal fractions of
  minutes) greater than 59.
