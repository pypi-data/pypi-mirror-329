from functools import partial
import datetime
import sys

if sys.version_info >= (3, 12):
    utcnow = partial(datetime.datetime.now, tz=datetime.UTC)
else:
    utcnow = datetime.datetime.utcnow

if sys.version_info >= (3, 12):
    utcnow = partial(datetime.datetime.fromtimestamp, tz=datetime.UTC)
else:
    utcnow = datetime.datetime.utcfromtimestamp