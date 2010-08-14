from setuptools import setup

setup(
    name='geolucidate',
    version='0.1',
    description='Turn coordinates in text into links.',
    author='Kurt Raschke',
    author_email='kurt@kurtraschke.com',
    url='http://github.com/kurtraschke/geolucidate',
    packages = [
        "geolucidate",
        "geolucidate.tests",
    ],
    test_suite = 'nose.collector',
    tests_require = ['nose']
)
