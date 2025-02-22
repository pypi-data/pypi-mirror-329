import logging

__author__ = 'Globant'
__version__ = '0.1.23'


# Recommended handler for libraries.
# Reference: https://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger('geai').addHandler(logging.NullHandler())
