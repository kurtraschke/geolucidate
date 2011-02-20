from urllib import urlencode


def default_link(url, text, title=''):
    '''
    The default link generating function, for generating HTML links as
    strings. To generate links as Genshi elements, lxml elements, etc.,
    supply an alternative link function which takes the same parameters.

    >>> default_link("http://www.google.com", "Google")
    u'<a href="http://www.google.com">Google</a>'

    >>> default_link("http://www.google.com", "Google", "Google")
    u'<a href="http://www.google.com" title="Google">Google</a>'

    '''
    if title is not '':
        title = u' title="{0}"'.format(title)
    return u"""<a href="{0}"{2}>{1}</a>""".format(url, text, title)


class MapLink(object):
    '''Convenience class for generating links to maps.
    >>> ml = MapLink("58147N/07720W", "58.235278", "-77.333333")
    >>> ml
    <MapLink 58.235278, -77.333333>
    '''

    def __init__(self, original_string, latitude, longitude):
        self.original_string = original_string
        self.lat_str = latitude
        self.long_str = longitude

    def coordinates(self, separator=''):
        return self.lat_str + separator + self.long_str

    def make_link(self, baseurl, params, link_generator):
        return link_generator(baseurl + urlencode(params.items()),
                              self.original_string,
                              u"{0} ({1})".format(self.original_string, self.coordinates(", ")))

    def __repr__(self):
        return "<MapLink %s>" % self.coordinates(", ")
