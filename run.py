import sys
import errno
from marshmallow.core.marshmallow import Marshmallow

try:
    assert sys.version_info >= (3, 6)
except AssertionError:
    print('Fatal Error: Wrong Python Version! Bot supports Python 3.6+!')
    exit(errno.EINVAL)

if __name__ == '__main__':
    marshmallow = Marshmallow()
    marshmallow.run()