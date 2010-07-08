geolucidate is a Python library for parsing coordinates in a variety
of input formats and returning a link to Google Maps or Bing.  This
was originally part of a larger project to parse the CADORS National
Report [1] into an Atom feed, but I am releasing it separately as I
envision it may be useful in a wide variety of applications.

[1]: http://wwwapps.tc.gc.ca/saf-sec-sur/2/cadors-screaq/m.aspx?lang=eng

The test cases in tests/tests.py have all been harvested from various
recent CADORS reports.  Some test cases which have been determined to
be invalid input have been commented out.
