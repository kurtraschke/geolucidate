geolucidate is a Python library for parsing coordinates in a variety
of input formats and returning a link to Google Maps or Bing.  This
was originally part of a larger project to parse the CADORS National
Report (see
http://wwwapps.tc.gc.ca/saf-sec-sur/2/cadors-screaq/m.aspx?lang=eng)
into an Atom feed, but I am releasing it separately as I envision it
may be useful in a wide variety of applications. There's no formal
specification for the input format; it's based on what I've observed
in CADORS reports and is fairly liberal.  If you have degrees,
minutes, and seconds (or a decimal fraction of minutes) in any
recognizable format, it should be parsed correctly.

The test cases in tests/tests.py have all been harvested from various
recent CADORS reports.  Some test cases which have been determined to
be invalid input have been commented out.
