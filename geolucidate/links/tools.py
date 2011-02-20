from urllib import urlencode


def default_link(url, text, title=''):
    '''
    The default link generating function, for generating HTML links as
    strings. To generate links as `Genshi <http://genshi.edgewall.org/>`_
    elements, `lxml <http://lxml.de/>`_ elements, etc., supply an
    alternate link-generating function which takes the same parameters.

    >>> default_link("http://www.google.com", "Google")
    u'<a href="http://www.google.com">Google</a>'

    >>> default_link("http://www.google.com", "Google", "Google")
    u'<a href="http://www.google.com" title="Google">Google</a>'

    '''
    if title is not '':
        title = u' title="{0}"'.format(title)
    return u"""<a href="{0}"{2}>{1}</a>""".format(url, text, title)


class MapLink(object):
    '''
    Convenience class for generating links to maps.

    >>> ml = MapLink("58147N/07720W", "58.235278", "-77.333333")
    >>> ml
    <MapLink 58.235278, -77.333333>

    '''

    lat_str = None
    """Latitude value, converted to a string.  Automatically quantized
    according to input precision."""
    long_str = None
    """Longitude value, converted to a string. Automatically quantized
    according to input precision."""
    original_string = None
    """Original string contaning parsed coordinates."""

    def __init__(self, original_string, latitude, longitude):
        '''
        Create a :class:`MapLink` with the given latitude, longitude,
        and original string.

        '''

        self.original_string = original_string
        self.lat_str = latitude
        self.long_str = longitude

    def coordinates(self, separator=''):
        '''
        Return the coordinates stored by this :class:`MapLink`, separated
        by optional separator character :obj:`separator`.

        '''
        return self.lat_str + separator + self.long_str

    def make_link(self, baseurl, params, link_generator):
        '''
        Calls the link generator function passed as :obj:`link_generator`
        to generate a link to the URL :obj:`baseurl`, with parameters
        :obj:`params`.

        The link text is set to the original string, while the
        link title is set to the original string followed by
        the parsed coordinates in parentheses.

        :param baseurl: Base URL to pass to link generator; should end in '?'
        :param params: Dictionary of parameters to be URL-encoded with
                       :func:`~urllib.urlencode` and appended to the base URL
        :param link_generator: Link-generating function; should take as
                               parameters the URL, text, and title, and return
                               generated HTML link

        >>> ml = MapLink("ABC123", "-10.0", "20.0")
        >>> ml.make_link("http://www.example.com/?",
        ...              {'foo': 'bar',
        ...               'lat': ml.lat_str,
        ...               'lon': ml.long_str},
        ...              default_link)
        u'<a href="http://www.example.com/?lat=-10.0&foo=bar&lon=20.0" title="ABC123 (-10.0, 20.0)">ABC123</a>'

        '''

        return link_generator(baseurl + urlencode(params.items()),
                              self.original_string,
                              u"{0} ({1})".format(self.original_string,
                                                  self.coordinates(", ")))

    def __repr__(self):
        return "<MapLink %s>" % self.coordinates(", ")
