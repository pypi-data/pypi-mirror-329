# pyfill
pyfill is a tool that detects Python versions and replaces deprecated features or standard libraries (e.g. datetime.utcnow) with alternative methods using only the standard library or Python itself whenever possible.
## Why this exists.
I use multiple libraries, such as apsig, to implement and use deprecated features to be able to use the library in multiple versions. However, this method does not allow the same deprecated feature to be reused when creating another library (except for copy and paste, etc.). To make this possible, this library is licensed and distributed under CC0.
## Current Features
- `datetime.utcnow()` (`pyfill.datetime.utcnow()`)
- `datetime.utcfromtimestamp()` (`pyfill.datetime.utcfromtimestamp()`)