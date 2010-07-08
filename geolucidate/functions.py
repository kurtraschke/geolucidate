# -*- coding: utf-8 -*-

import re
from decimal import Decimal, getcontext
from parser import parser_re

def cleanup(parts):
    latdir = (parts['latdir'] or parts['latdir2']).upper()
    longdir = (parts['longdir'] or parts['longdir2']).upper()

    latdir = latdir[0]
    longdir = longdir[0]

    latdeg = parts.get('latdeg','00')

    longdeg = parts.get('longdeg','00')

    latmin = parts.get('latmin','00') or '00'
    longmin = parts.get('longmin','00') or '00'

    latdecsec = parts.get('latdecsec','')
    longdecsec = parts.get('longdecsec','')

    if (latdecsec and longdecsec):
        latmin += latdecsec
        longmin += longdecsec
        latsec = '00'
        longsec = '00'
    else:
        latsec = parts.get('latsec','') or '00'
        longsec = parts.get('longsec','') or '00'

    return [latdir, latdeg, latmin, latsec, longdir, longdeg, longmin, longsec]

def convert(latdir, latdeg, latmin, latsec, longdir, longdeg, longmin, longsec):
    """
    >>> convert('N','50','30','30','W','50','30','30')
    (Decimal('50.50833333'), Decimal('-50.50833333'))

    """
    getcontext().prec=10

    latitude = Decimal(latdeg)
    
    latsec =  Decimal(latsec) / Decimal('60')
    latitude += (Decimal(latmin) + latsec) / Decimal('60')

    if latdir == 'S':
        latitude *= Decimal('-1')

    longitude = Decimal(longdeg)
    
    longsec =  Decimal(longsec) / Decimal('60')
    longitude += (Decimal(longmin) + longsec) / Decimal('60')

    if longdir == 'W':
        longitude *= Decimal('-1')
        
    return (latitude, longitude)

def google_maps_link(type="m"):
    def func(original_string, latitude, longitude):
        coord_str = str(latitude.quantize(Decimal('0.000001')))+","+str(longitude.quantize(Decimal('0.000001')))
        return """<a href="http://maps.google.com/maps?q={0}&ll={0}&t={1}">{2}</a>""".format(coord_str,
                                                                                             type,
                                                                                             original_string)
    return func

def bing_maps_link(style='r'):
    def func(original_string, latitude, longitude):
        coord_str = str(latitude.quantize(Decimal('0.000001')))+"~"+str(longitude.quantize(Decimal('0.000001')))
        return """<a href="http://bing.com/maps/default.aspx?v=2&cp={0}&style={1}&sp=Point.{3}_{4}_{2}">{2}</a>""".format(
            coord_str,
            style,
            original_string,
            str(latitude.quantize(Decimal('0.000001'))),
            str(longitude.quantize(Decimal('0.000001')))
            )
    return func
    

def replace(string, sub_function=google_maps_link()):
    """
    >>> replace("58147N/07720W")
    '<a href="http://maps.google.com/maps?q=58.235278,-77.333333&ll=58.235278,-77.333333&t=m">58147N/07720W</a>'

    >>> replace("58147N/07720W", google_maps_link('k'))
    '<a href="http://maps.google.com/maps?q=58.235278,-77.333333&ll=58.235278,-77.333333&t=k">58147N/07720W</a>'

    >>> replace("58147N/07720W", bing_maps_link('a'))
    '<a href="http://bing.com/maps/default.aspx?v=2&cp=58.235278~-77.333333&style=a&sp=Point.58.235278_-77.333333_58147N/07720W">58147N/07720W</a>'


    """

    def do_replace(match):
        original_string = match.group()
        (latitude, longitude) = convert(*cleanup(match.groupdict()))
        return sub_function(original_string, latitude, longitude)

    return parser_re.sub(do_replace, string)
