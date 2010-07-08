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

def convert(parts):
    getcontext().prec=10

    (latdir, latdeg, latmin, latsec, longdir, longdeg, longmin, longsec) = parts

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

def stringify(latitude, longitude):
    return str(latitude.quantize(Decimal('0.000001')))+","+str(longitude.quantize(Decimal('0.000001')))

def replace(m):
    parts = cleanup(m.groupdict())
    coordinates = stringify(*convert(parts))
    return m.expand("""<a href="http://maps.google.com/maps?q=%s">\g<0></a>""" % coordinates)
