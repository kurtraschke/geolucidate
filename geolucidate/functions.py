# -*- coding: utf-8 -*-

import re
from decimal import Decimal, setcontext, ExtendedContext
from urllib import urlencode
from geolucidate.parser import parser_re
from geolucidate.links.google import google_maps_link
from geolucidate.links.bing import bing_maps_link
from geolucidate.links.tools import MapLink


setcontext(ExtendedContext)


def _cleanup(parts):
    """
    Normalize up the parts matched by :obj:`parser.parser_re` to
    degrees, minutes, and seconds.

    >>> _cleanup({'latdir': 'south', 'longdir': 'west',
    ...          'latdeg':'60','latmin':'30',
    ...          'longdeg':'50','longmin':'40'})
    ['S', '60', '30', '00', 'W', '50', '40', '00']

    >>> _cleanup({'latdir': 'south', 'longdir': 'west',
    ...          'latdeg':'60','latmin':'30', 'latdecsec':'.50',
    ...          'longdeg':'50','longmin':'40','longdecsec':'.90'})
    ['S', '60', '30.50', '00', 'W', '50', '40.90', '00']

    """

    latdir = (parts['latdir'] or parts['latdir2']).upper()[0]
    longdir = (parts['longdir'] or parts['longdir2']).upper()[0]

    latdeg = parts.get('latdeg')
    longdeg = parts.get('longdeg')

    latmin = parts.get('latmin', '00') or '00'
    longmin = parts.get('longmin', '00') or '00'

    latdecsec = parts.get('latdecsec', '')
    longdecsec = parts.get('longdecsec', '')

    if (latdecsec and longdecsec):
        latmin += latdecsec
        longmin += longdecsec
        latsec = '00'
        longsec = '00'
    else:
        latsec = parts.get('latsec', '') or '00'
        longsec = parts.get('longsec', '') or '00'

    return [latdir, latdeg, latmin, latsec, longdir, longdeg, longmin, longsec]


def _convert(latdir, latdeg, latmin, latsec,
            longdir, longdeg, longmin, longsec):
    """
    Convert normalized degrees, minutes, and seconds to decimal degrees.
    Quantize the converted value based on the input precision and
    return a 2-tuple of strings.

    >>> _convert('S','50','30','30','W','50','30','30')
    ('-50.508333', '-50.508333')

    """
    latitude = Decimal(latdeg)
    latitude += (Decimal(latmin) +
                 (Decimal(latsec) / Decimal('60'))) / Decimal('60')

    if latdir == 'S':
        latitude *= Decimal('-1')

    longitude = Decimal(longdeg)
    longitude += (Decimal(longmin) +
                  (Decimal(longsec) / Decimal('60'))) / Decimal('60')

    if longdir == 'W':
        longitude *= Decimal('-1')

    if (latsec != '00' or longsec != '00'):
        precision = Decimal('0.000001')
    elif (latmin != '00' or longmin != '00'):
        precision = Decimal('0.001')
    else:
        precision = Decimal('1')

    lat_str = str(latitude.quantize(precision))
    long_str = str(longitude.quantize(precision))

    return (lat_str, long_str)


def replace(string, sub_function=google_maps_link()):
    """
    Replace detected coordinates with a map link, using the given substitution
    function.

    The substitution function will be passed a :class:`~.MapLink` instance, and
    should return a string which will be substituted by :func:`re.sub` in place
    of the detected coordinates.

    >>> replace("58147N/07720W")
    u'<a href="http://maps.google.com/maps?q=58.235278%2C-77.333333+%2858147N%2F07720W%29&ll=58.235278%2C-77.333333&t=h" title="58147N/07720W (58.235278, -77.333333)">58147N/07720W</a>'

    >>> replace("5814N/07720W", google_maps_link('satellite'))
    u'<a href="http://maps.google.com/maps?q=58.233%2C-77.333+%285814N%2F07720W%29&ll=58.233%2C-77.333&t=k" title="5814N/07720W (58.233, -77.333)">5814N/07720W</a>'

    >>> replace("58N/077W", bing_maps_link('map'))
    u'<a href="http://bing.com/maps/default.aspx?style=r&cp=58%7E-77&sp=Point.58_-77_58N%2F077W&v=2" title="58N/077W (58, -77)">58N/077W</a>'

    """

    def do_replace(match):
        original_string = match.group()
        (latitude, longitude) = _convert(*_cleanup(match.groupdict()))
        return sub_function(MapLink(original_string, latitude, longitude))

    return parser_re.sub(do_replace, string)


def get_replacements(string, sub_function=google_maps_link()):
    """
    Return a dict whose keys are instances of :class:`re.MatchObject` and
    whose values are the corresponding replacements.  Use
    :func:`get_replacements` when the replacement cannot be performed
    through ordinary string substitution by :func:`re.sub`, as in
    :func:`replace`.


    >>> get_replacements("4630 NORTH 5705 WEST 58147N/07720W")
    ... #doctest: +ELLIPSIS
    {<_sre.SRE_Match object at ...>: u'<a href="..." title="...">4630 NORTH 5705 WEST</a>', <_sre.SRE_Match object at ...>: u'<a href="..." title="...">58147N/07720W</a>'}

    >>> string = "4630 NORTH 5705 WEST 58147N/07720W"
    >>> replacements = get_replacements(string)
    >>> offset = 0
    >>> from UserString import MutableString
    >>> out = MutableString(string)
    >>> for (match, link) in replacements.iteritems():
    ...     start = match.start() + offset
    ...     end = match.end() + offset
    ...     out[start:end] = link
    ...     offset += (len(link) - len(match.group()))
    >>> out == replace(string)
    True
    """

    substitutions = {}
    matches = parser_re.finditer(string)

    for match in matches:
        (latitude, longitude) = _convert(*_cleanup(match.groupdict()))
        substitutions[match] = sub_function(MapLink(match.group(),
                                                    latitude, longitude))

    return substitutions
