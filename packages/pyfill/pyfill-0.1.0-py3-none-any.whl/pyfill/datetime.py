import datetime
import sys

def utcnow() -> datetime:
    """Construct a UTC datetime from time.time()."""
    if sys.version_info >= (3, 12):
        return datetime.datetime.now(datetime.UTC)
    return datetime.datetime.utcnow()

def utcfromtimestamp() -> datetime:
    """Construct a UTC datetime from time.time()."""
    if sys.version_info >= (3, 12):
        return datetime.datetime.fromtimestamp(datetime.UTC)
    return datetime.datetime.utcfromtimestamp()