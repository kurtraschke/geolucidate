# -*- coding: utf-8 -*-

import re
from decimal import Decimal, getcontext
from urllib import urlencode
from parser import parser_re


def cleanup(parts):
    """
    >>> cleanup({'latdir': 'south', 'longdir': 'west',
    ...          'latdeg':'60','latmin':'30',
    ...          'longdeg':'50','longmin':'40'})
    ['S', '60', '30', '00', 'W', '50', '40', '00']

    >>> cleanup({'latdir': 'south', 'longdir': 'west',
    ...          'latdeg':'60','latmin':'30', 'latdecsec':'.50',
    ...          'longdeg':'50','longmin':'40','longdecsec':'.90'})
    ['S', '60', '30.50', '00', 'W', '50', '40.90', '00']

    """

    latdir = (parts['latdir'] or parts['latdir2']).upper()
    longdir = (parts['longdir'] or parts['longdir2']).upper()

    latdir = latdir[0]
    longdir = longdir[0]

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


def convert(latdir, latdeg, latmin, latsec,
            longdir, longdeg, longmin, longsec):
    """
    >>> convert('S','50','30','30','W','50','30','30')
    (Decimal('-50.50833333'), Decimal('-50.50833333'))

    """
    getcontext().prec = 10

    latitude = Decimal(latdeg)

    latsec = Decimal(latsec) / Decimal('60')
    latitude += (Decimal(latmin) + latsec) / Decimal('60')

    if latdir == 'S':
        latitude *= Decimal('-1')

    longitude = Decimal(longdeg)

    longsec = Decimal(longsec) / Decimal('60')
    longitude += (Decimal(longmin) + longsec) / Decimal('60')

    if longdir == 'W':
        longitude *= Decimal('-1')

    return (latitude, longitude)


def default_link(url, text, title=''):
    """
    >>> default_link("http://www.google.com", "Google")
    '<a href="http://www.google.com">Google</a>'

    >>> default_link("http://www.google.com", "Google", "Google")
    '<a href="http://www.google.com" title="Google">Google</a>'

    """
    if title is not '':
        title = ' title="{0}"'.format(title)
    return """<a href="{0}"{2}>{1}</a>""".format(url, text, title)


class MapLink(object):

    PRECISION = Decimal('0.000001')

    def __init__(self, original_string, latitude, longitude):
        self.original_string = original_string
        self.latitude = latitude
        self.longitude = longitude
        self.lat_str = str(self.latitude.quantize(self.PRECISION))
        self.long_str = str(self.longitude.quantize(self.PRECISION))

    def coordinates(self, separator):
        return self.lat_str + separator + self.long_str

    def make_link(self, baseurl, params, link_generator):
        return link_generator(baseurl + urlencode(params.items()),
                              self.original_string,
                              self.coordinates(", "))


def google_maps_link(type='hybrid'):
    types = {'map': 'm', 'satellite': 'k', 'hybrid': 'h'}

    def func(maplink, link=default_link):
        baseurl = "http://maps.google.com/maps?"
        coordinates = maplink.coordinates(',')
        params = {'q': "{0} ({1})".format(coordinates,
                                          maplink.original_string),
                  'll': coordinates,
                  't': types[type]}
        return maplink.make_link(baseurl, params, link)
    return func


def bing_maps_link(type='hybrid'):
    types = {'map': 'r', 'satellite': 'a', 'hybrid': 'h'}

    def func(maplink, link=default_link):
        baseurl = "http://bing.com/maps/default.aspx?"
        params = {'v': '2',
                  'cp': maplink.coordinates("~"),
                  'style':  types[type],
                  'sp': "Point.{1}_{2}_{0}".format(maplink.original_string,
                                                   maplink.lat_str,
                                                   maplink.long_str)}
        return maplink.make_link(baseurl, params, link)
    return func


def replace(string, sub_function=google_maps_link()):
    """
    >>> replace("58147N/07720W")
    '<a href="http://maps.google.com/maps?q=58.235278%2C-77.333333+%2858147N%2F07720W%29&ll=58.235278%2C-77.333333&t=h" title="58.235278, -77.333333">58147N/07720W</a>'

    >>> replace("58147N/07720W", google_maps_link('satellite'))
    '<a href="http://maps.google.com/maps?q=58.235278%2C-77.333333+%2858147N%2F07720W%29&ll=58.235278%2C-77.333333&t=k" title="58.235278, -77.333333">58147N/07720W</a>'

    >>> replace("58147N/07720W", bing_maps_link('map'))
    '<a href="http://bing.com/maps/default.aspx?style=r&cp=58.235278%7E-77.333333&sp=Point.58.235278_-77.333333_58147N%2F07720W&v=2" title="58.235278, -77.333333">58147N/07720W</a>'

    """

    def do_replace(match):
        original_string = match.group()
        (latitude, longitude) = convert(*cleanup(match.groupdict()))
        return sub_function(MapLink(original_string, latitude, longitude))

    return parser_re.sub(do_replace, string)


def get_replacements(string, link_function=default_link,
                     sub_function=google_maps_link()):
    """
    >>> get_replacements("4630 NORTH 5705 WEST 58147N/07720W")
    ... #doctest: +ELLIPSIS
    {<_sre.SRE_Match object at ...>: '<a href="..." title="...">4630 NORTH 5705 WEST</a>', <_sre.SRE_Match object at ...>: '<a href="..." title="...">58147N/07720W</a>'}

    """

    substitutions = {}

    matches = parser_re.finditer(string)

    for match in matches:
        (latitude, longitude) = convert(*cleanup(match.groupdict()))
        substitutions[match] = sub_function(MapLink(match.group(),
                                                    latitude, longitude),
                                            link_function)

    return substitutions
