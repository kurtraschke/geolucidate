# -*- coding: utf-8 -*-

"""
This module contains the regular expression which is used by
geolucidate to identify and extract geographic coordinates.

It is a point of some pride for the author that despite the
diversity of formats accepted by geolucidate, only a single regular
expression is needed to parse all of them.  This has, however,
resulted in a rather lengthy and complex regular expression.

"""

import re

parser_re = re.compile(ur"""\b
    # Latitude direction, first position: one of N, S, NORTH, SOUTH
    (?P<latdir>NORTH|SOUTH|[NS])?
    # Latitude degrees: two digits 0-90
    (?P<latdeg>([0-8][0-9])|90)
    # Optional space, degree mark, period,
    # or word separating degrees and minutes
    (\ |(?P<degmark>\ ?(º|°)\ ?|\.|-|\ DEGREES,\ ))?
    (?P<latminsec>
    # Latitude minutes: two digits 0-59
    (?P<latmin>[0-5][0-9])
    # If there was a degree mark before, look for punctuation after the minutes
    (\ |(?(degmark)('|"|\.|\ MINUTES(,\ )?)))?
    (
    # Latitude seconds: two digits 0-59
    ((?P<latsec>([0-9]|[0-5][0-9]))|
    # Decimal fraction of minutes
    (?P<latdecsec>\.\d{1,3}))?)
    (?(degmark)("|'|\ SECONDS\ )?)
    )?
    # Latitude direction, second position, optionally preceded by a space
    (\ ?(?P<latdir2>(?(latdir)|(NORTH|SOUTH|[NS]))))
    # Latitude/longitude delimiter: space, forward slash, comma, or none
    (\ ?[ /]\ ?|,\ )?
    # Longitude direction, first position: one of N, S, NORTH, SOUTH
    (?(latdir)(?P<longdir>EAST|WEST|[EW]))
    # Longitude degrees: two or three digits
    (?P<longdeg>\d{2,3})
    # If there was a degree mark before, look for another one here
    (\ |(?(degmark)(\ ?(º|°)\ ?|\.|-|\ DEGREES,\ )))?
    (?(latminsec)   #Only look for minutes and seconds in the longitude
    (?P<longminsec> #if they were there in the latitude
    # Longitude minutes: two digits
    (?P<longmin>[0-5][0-9])
    # If there was a degree mark before, look for punctuation after the minutes
    (\ |(?(degmark)('|"|\.|\ MINUTES(,\ )?)))?
    # Longitude seconds: two digits 0-59
    ((?P<longsec>([0-9][0-9]))|
    # Decimal fraction of minutes
    (?P<longdecsec>\.\d{1,3}))?)
    (?(degmark)("|'|\ SECONDS\ )?)
    )
    #Longitude direction, second position: optionally preceded by a space
    (?(latdir)|\ ?(?P<longdir2>(EAST|WEST|[EW])))
    \b
    """, re.VERBOSE | re.UNICODE | re.IGNORECASE)
"""The coordinate-parsing regular expression,
compiled with :func:`re.compile`"""
