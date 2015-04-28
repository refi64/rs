try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name='rs',
    author='Ryan Gonzalez',
    description='A simple sed-like alternative with full Perl regexes',
    classifiers=['License :: OSI Approved :: MIT License'],
    scripts=['rs.py']
)
