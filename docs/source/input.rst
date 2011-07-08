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

* 'Seconds' which are preceded by a decimal point, which are greater
  than 59, or which are three digits long will be treated as a decimal
  fraction of minutes; that is, they will be divided by 100 rather
  than 60.  If a period is used to separate degrees and minutes, then
  any period present between the minutes and seconds is taken as a
  separator, rather than a decimal point.  Several examples may help
  to clarify this point:

  - ``N51.33.9`` is parsed as 51 degrees, 33 minutes, and 9 seconds,
    because a period is used to separate the degrees and minutes, and
    the value in the seconds position is less than 60.

  - ``N50.26.008`` is parsed as 51 degrees, 26.008 minutes.  This is
    because the 'seconds' value is three digits long.

  - ``49-21.834N`` is parsed as 49 degrees, 21.834 minutes.  Again,
    this is due to the presence of a decimal point and a three-digit
    'seconds' value.

  - ``N53 35.48`` is parsed as 53 degrees, 35.48 minutes.  Despite the
    fact that the 'seconds' value is only two digits long and less
    than 60, the fact that there is no period used between the degrees
    and minutes is taken to mean that the period which is found
    between the minutes and 'seconds' is actually a decimal point.

* Degree marks and punctuation following minutes and seconds are only
  accepted if a degree mark is present following the latitude
  degrees.  The effect of this is that the use of degree
  marks/punctuation must be consistent.

* Numeric values must be within sensible ranges; degrees greater than
  90 for latitude or 180 for longitude are not accepted; nor are minutes
  or seconds (subject to the caveat above regarding decimal fractions of
  minutes) greater than 59.
