# -*- coding: utf-8 -*-

from geolucidate.functions import _cleanup
from geolucidate.parser import parser_re

from nose.tools import eq_


def test_parser():
    values = [
        ("N424400 W800557", ['N', '42', '44', '00', 'W', '80', '05', '57']),
        ("4745N/6440W", ['N', '47', '45', '00', 'W', '64', '40', '00']),
        ("4523N/07319W", ['N', '45', '23', '00', 'W', '073', '19', '00']),
        ("5335N / 12155W ", ['N', '53', '35', '00', 'W', '121', '55', '00']),
        ("58147N/07720W", ['N', '58', '14', '7', 'W', '077', '20', '00']),
        ("462716N/0721147W", ['N', '46', '27', '16', 'W', '072', '11', '47']),
        ("491500N 1230720W", ['N', '49', '15', '00', 'W', '123', '07', '20']),
        ("5046.6N / 06829.2W", ['N', '50', '46.6', '00', 'W', '068', '29.2', '00']),
        ("5734.8 N / 10006.2 W", ['N', '57', '34.8', '00', 'W', '100', '06.2', '00']),
        ("(4952.013N / 09548.474W)", ['N', '49', '52.013', '00', 'W', '095', '48.474', '00']),
        ("N4909.44 W12210.13",['N', '49', '09.44', '00', 'W', '122', '10.13', '00']),
        ("6535.26N/08801.25W", ['N', '65', '35.26', '00', 'W', '088', '01.25', '00']),
        ("5033.15N 11544.09W", ['N', '50', '33.15', '00', 'W', '115', '44.09', '00']),
        ("N53 35.48 W112 02.60", ['N', '53', '35.48', '00', 'W', '112', '02.60', '00']),
        ("52 degrees, 42 minutes north, 124 degrees, 50 minutes west",
         ['N', '52', '42', '00', 'W', '124', '50', '00']),
        ("5115N8940W", ['N', '51', '15', '00', 'W', '89', '40', '00']),
        ("4630 NORTH 5705 WEST", ['N', '46', '30', '00', 'W', '57', '05', '00']),
        ("6146 north 5328 west", ['N', '61', '46', '00', 'W', '53', '28', '00']),
        ("52 North 50 West", ['N', '52', '00', '00', 'W', '50', '00', '00']),
        (u"70 ° 57N 070 ° 05W", ['N', '70', '57', '00', 'W', '070', '05', '00']),
        (u"""(45º10'17"N 076º23'46"W)""", ['N', '45', '10', '17', 'W', '076', '23', '46']),
        #Note that the degree and minute punctuation are actually backwards; we support it anyway.
        (u"""(45º10"17'N 076º23"46'W" """, ['N', '45', '10', '17', 'W', '076', '23', '46']),
        (u"43º55'N 078º18'W", ['N', '43', '55', '00', 'W', '078', '18', '00']),
        (u"43º01N 081º46W", ['N', '43', '01', '00', 'W', '081', '46', '00']),
        (u"""49º41'34"N 093º37'54"W""", ['N', '49', '41', '34', 'W', '093', '37', '54']),
        ("(N51.33.9 W119.02.30)", ['N', '51', '33', '9', 'W', '119', '02', '30']),
        ("49-21.834N 126-15.923W", ['N', '49', '21.834', '00', 'W', '126', '15.923', '00']),
        (u"(40º02.247'N 111º44.383'W)", ['N', '40', '02.247', '00', 'W', '111', '44.383', '00']),
        ("N495342 / W0742553", ['N', '49', '53', '42', 'W', '074', '25', '53']),
        #No direction given for latitude and longitude;
        #are we to assume north and west?
        #(u"""(43º52'43"/079º48'13")""", ['',  '43',  '52',  '43',  '',  '079',  '48',  '13']),
        #You can't have 65 seconds.
        #("50 27 55 N 127 27 65 W", ['N', '50', '27', '55', 'W', '127', '27', '65']),
        #We still use the same format as a test case.
        ("50 27 55 N 127 27 59 W", ['N', '50', '27', '55', 'W', '127', '27', '59']),
        #Another oddball with impossible seconds; I really wonder where these come from.
        #("513390N 1190230W", ['N', '51', '33', '90', 'W', '119', '02', '30']),
        #Possibly missing something; 7º W isn't anywhere near Canada.
        #("5617N/0721W", ['N', '56', '17', '00', 'W', '07', '21', '00']),
        #Latitude and longitude reversed.
        #("10626W / 5156N",  ['N', '', '', '', 'W', '', '', '']),
        #Longitude seconds (78) impossible.
        #("491129N 1230778W",  ['N', '49', '11', '29', 'W', '123', '07', '78']),
        #Longitude seconds (95) impossible.
        #("484819N 1231195W",  ['N', '48', '48', '13', 'W', '123', '11', '95']),
        ]

    for test in values:
        (coord_string, result) = test
        yield check_parser, coord_string, result


def check_parser(coord_string, result):
    match = parser_re.search(coord_string)
    assert match
    eq_(_cleanup(match.groupdict()), result)


def test_false_positive():
    values = ["GGN7383 was", "6830N 70W"]
    for test in values:
        yield check_false_positive, test


def check_false_positive(test):
    match = parser_re.search(test)
    eq_(match, None)
