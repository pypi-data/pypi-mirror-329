# pyfill
pyfill is a tool that detects Python versions and replaces deprecated features or standard libraries (e.g. datetime.utcnow) with alternative methods using only the standard library or Python itself whenever possible.
## Why this exists
I use deprecated features in the process of maintaining multiple libraries, such as apsig, and then use the same features in multiple versions by replacing them with alternative features in deprecated and subsequent versions. However, this method does not allow me to reuse the same deprecated features when creating another library (except for copy/paste, etc.). To make this possible, this library is licensed under CC0.
## Current Features
- `datetime.utcnow()` (`pyfill.datetime.utcnow()`)
- `datetime.utcfromtimestamp()` (`pyfill.datetime.utcfromtimestamp()`)
## Other Alternatives
[`audioop-lts`](https://github.com/AbstractUmbra/audioop): LTS port for the audioop module, which was removed in 3.13 and deprecated in 3.11.
