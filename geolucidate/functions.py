import re
from decimal import Decimal, getcontext

def parse(string):
    coord = re.compile(u"""
    # Latitude direction, first position: one of N, S, NORTH, SOUTH
    (?P<latdir>NORTH|SOUTH|[NS])?                    
    # Latitude degrees: two digits 0-90
    (?P<latdeg>([0-8][0-9])|90)
    # Optional space or degree mark separating degrees and minutes
    (\ |(?P<degmark>º|\ DEGREES,\ ))?
    (?P<latminsec>
    # Latitude minutes: two digits 0-59
    (?P<latmin>[0-5][0-9])
    # If there was a degree mark before, look for punctuation after the minutes
    (?(degmark)(\'|\ MINUTES(,\ )?))?
    (
    # Latitude seconds: two digits 0-59
    (?P<latsec>([0-9]|[0-5][0-9]))(?(degmark)("|\ SECONDS\ ))|
    # Decimal fraction of minutes
    (?P<latdecsec>\\.\\d{1,2}))?
    )?
    # Latitude direction, second position, optionally preceded by a space
    (\ ?(?P<latdir2>(?(latdir)|(NORTH|SOUTH|[NS]))))
    # Latitude/longitude delimiter: space, forward slash, comma, or none
    (\ ?[ /]\ ?|,\ )?
    # Longitude direction, first position: one of N, S, NORTH, SOUTH
    (?P<longdir>EAST|WEST|[EW])?
    # Longitude degrees: two or three digits
    (?P<longdeg>\\d{2,3}?)
    # If there was a degree mark before, look for another one here
    (\ |(?(degmark)(º|\ DEGREES,\ )))?
    (?(latminsec) #Only look for minutes and seconds in the longitude if they were there in the latitude
    (?P<longminsec>
    # Longitude minutes: two digits
    (?P<longmin>[0-5][0-9])
    # If there was a degree mark before, look for punctuation after the minutes
    (?(degmark)('|\ MINUTES(,\ )?))?
    # Longitude seconds: two digits 0-59
    ((?P<longsec>([0-5][0-9]))(?(degmark)("|\ SECONDS\ ))|
    # Decimal fraction of minutes
    (?P<longdecsec>\\.\\d{1,2}))?
    ))
    #Longitude direction, second position: optionally preceded by a space
    ((?(longdir)|\ ?(?P<longdir2>(EAST|WEST|[EW]))))
    """,re.VERBOSE|re.UNICODE|re.IGNORECASE)

    r = coord.search(string)
    parts = r.groupdict()

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
