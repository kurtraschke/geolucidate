from geolucidate.links.tools import default_link


def google_maps_link(type='hybrid', link=default_link):
    '''
    Returns a function for generating links to Google Maps.

    :param type: map type, one of  'map', 'satellite', or 'hybrid'
    :param link: Link-generating function; defaults to :func:`~.default_link`

    >>> from .tools import MapLink
    >>> google_maps_link()(MapLink("CN Tower", "43.6426", "-79.3871"))
    u'<a href="http://maps.google.com/maps?q=43.6426%2C-79.3871+%28CN+Tower%29&ll=43.6426%2C-79.3871&t=h" title="CN Tower (43.6426, -79.3871)">CN Tower</a>'
    '''
    types = {'map': 'm', 'satellite': 'k', 'hybrid': 'h'}

    def func(maplink):
        baseurl = "http://maps.google.com/maps?"
        coordinates = maplink.coordinates(',')
        params = {'q': u"{0} ({1})".format(coordinates,
                                           maplink.original_string).encode('utf-8'),
                  'll': coordinates,
                  't': types[type]}
        return maplink.make_link(baseurl, params, link)
    return func
