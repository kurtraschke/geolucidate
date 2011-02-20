from geolucidate.links.tools import default_link


def bing_maps_link(type='hybrid', link=default_link):
    """
    Returns a function for generating links to Bing Maps.

    :param type: map type, one of  'map', 'satellite', or 'hybrid'
    :param link: link-generating function; defaults to :func:`~.default_link`

    >>> from .tools import MapLink
    >>> bing_maps_link()(MapLink("CN Tower", "43.6426", "-79.3871"))
    u'<a href="http://bing.com/maps/default.aspx?style=h&cp=43.6426%7E-79.3871&sp=Point.43.6426_-79.3871_CN+Tower&v=2" title="CN Tower (43.6426, -79.3871)">CN Tower</a>'

    """
    types = {'map': 'r', 'satellite': 'a', 'hybrid': 'h'}

    def func(maplink, link=default_link):
        baseurl = "http://bing.com/maps/default.aspx?"
        params = {'v': '2',
                  'cp': maplink.coordinates("~"),
                  'style': types[type],
                  'sp': u"Point.{1}_{2}_{0}".format(maplink.original_string,
                                                    maplink.lat_str,
                                                    maplink.long_str).encode('utf-8')}
        return maplink.make_link(baseurl, params, link)
    return func
