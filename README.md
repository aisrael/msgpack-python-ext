# MsgPack Python Ext

[![PyPi](https://img.shields.io/pypi/v/msgpack-python-ext.svg)](https://pypi.python.org/pypi/msgpack-python-ext)

[![Travis CI](https://img.shields.io/travis/aisrael/msgpack-python-ext.svg)](https://travis-ci.org/aisrael/msgpack-python-ext)

[![Documentation Status](https://readthedocs.org/projects/msgpack-python-ext/badge/?version=latest)](https://msgpack-python-ext.readthedocs.io/en/latest/?badge=latest)

[![Updates](https://pyup.io/repos/github/aisrael/msgpack-python-ext/shield.svg)](https://pyup.io/repos/github/aisrael/msgpack-python-ext/)

[`msgpack-python`](https://github.com/msgpack/msgpack-python) extension that provides support for Timestamp, Date, and "Naive" DateTime (UTC) packed Ext types.

-   Free software: BSD license
-   Documentation: https://msgpack-python-ext.readthedocs.io.

## Usage

Until this project is published on PyPI, simply add the following to your `requirements.txt`:

```
git+https://github.com/aisrael/msgpack-python-ext
```

Then, instead of using `msgpack.packb`/`msgpack.unpackb` directly, you would use `msgpack_ext.packb`/`msgpack_ext.unpackb` as follows:

```
import datetime
import msgpack_ext

packed_date = msgpack_ext.packb(datetime.date(2008, 8, 16))
assert b'\xd6e\x07\xd8\x08\x10' == packed_date

date = msgpack_ext.unpackb(packed_date)
assert datetime.date(2008, 8, 16) == date

packed_datetime = msgpack_ext.packb(datetime.datetime(1879, 3, 14, 11, 30, 00))
assert b'\xc7\x06f\x07W\x03\x0e\xa1\xb8' == packed_datetime

dt = msgpack_ext.unpackb(packed_datetime)
assert datetime.datetime(1879, 3, 14, 11, 30, 00) == dt
```

`msgpack_ext.unpackb` adds the `ext_hook = msgpack_ext.msgpack_ext.ext_hook` keyword option automatically to provide an `ext_hook` that can recognize and succesfully unpack date, datetime, and the MessagePack Timestamp Ext formats.

## Date and DateTime formats

For all dates, times, and timestamps, assume UTC from the sender.

Dates are packed/unpacked using the Ext type with code `101` using the following format:

```
| year (uint64) | month (uint8) | day (uint8) |
```

DateTimes are Dates are packed/unpacked using the Ext type with code `102` using the following format:

```
| year (uint64) | month (uint8) | day (uint8) | seconds_from_midnight (uint32) |
```

### Credits

This package was created with [Cookiecutter] and the [`audreyr/cookiecutter-pypackage`] project template.

[cookiecutter]: https://github.com/audreyr/cookiecutter
[`audreyr/cookiecutter-pypackage`]: https://github.com/audreyr/cookiecutter-pypackage
