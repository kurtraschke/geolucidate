from geolucidate.links.tools import default_link


def openstreetmap_link(link=default_link):
    '''
    Returns a function for generating links to OpenStreetMap.

    :param link: Link-generating function; defaults to :func:`~.default_link`

    >>> from .tools import MapLink
    >>> openstreetmap_link()(MapLink("CN Tower", "43.6426", "-79.3871"))
    u'<a href="http://www.openstreetmap.org/?mlat=43.6426&mlon=-79.3871&zoom=9" title="CN Tower (43.6426, -79.3871)">CN Tower</a>'
    '''

    def func(maplink, link=default_link):
        baseurl = "http://www.openstreetmap.org/?"
        params = {'mlat': maplink.lat_str,
                  'mlon': maplink.long_str,
                  'zoom': '9'}
        return maplink.make_link(baseurl, params, link)
    return func
