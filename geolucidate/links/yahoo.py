from geolucidate.links.tools import default_link


def yahoo_maps_link(type='hybrid', link=default_link):
    '''
    Returns a function for generating links to Yahoo Maps.

    :param type: map type, one of  'map', 'satellite', or 'hybrid'
    :param link: Link-generating function; defaults to :func:`~.default_link`

    >>> from .tools import MapLink
    >>> yahoo_maps_link()(MapLink("CN Tower", "43.6426", "-79.3871"))
    u'<a href="http://maps.yahoo.com/#lat=43.6426&lon=-79.3871&mvt=h&zoom=10&q1=43.6426%2C-79.3871" title="CN Tower (43.6426, -79.3871)">CN Tower</a>'
    '''

    types = {'map': 'm', 'satellite': 's', 'hybrid': 'h'}

    def func(maplink, link=default_link):
        baseurl = "http://maps.yahoo.com/#"
        params = {'mvt': types[type],
                  'lat': maplink.lat_str,
                  'lon': maplink.long_str,
                  'zoom': '10',
                  'q1': maplink.coordinates(",")}
        return maplink.make_link(baseurl, params, link)
    return func
