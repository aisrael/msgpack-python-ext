"""Top-level package for MsgPack Python Ext."""

__author__ = """Alistair A. Israel"""
__email__ = 'aisrael@gmail.com'
__version__ = '0.1.0'

import msgpack as _msgpack
from msgpack_ext.msgpack_ext import default, ext_hook, EXT_CODE_DATE, EXT_CODE_DATETIME


def packb(o, **kwargs):
    """
    Pack object `o` and return packed bytes
    """
    kwargs['default'] = default
    return _msgpack.packb(o, **kwargs)


def unpackb(packed, **kwargs):
    """
    Unpack an object from `packed`. Adds `ext_hook = msgpack_ext.ext_hook`

    See `msgpack.unpackb` for details.
    """
    kwargs['ext_hook'] = ext_hook
    return _msgpack.unpackb(packed, **kwargs)
