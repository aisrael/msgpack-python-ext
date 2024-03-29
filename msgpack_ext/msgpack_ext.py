"""Main module."""

import datetime
import struct

from msgpack import ExtType

EXT_CODE_DATE = 101
EXT_CODE_DATETIME = 102


def pack_date(date):
    """
    Packs a date (assumed to be UTC) as a struct with of 16-bit, unsigned `year`
    (big endian), 1 byte `month`, and 1 byte `day`.
    """
    return struct.pack("!HBB", date.year, date.month, date.day)


def unpack_date(packed):
    """
    Unpacks a UTC date packed as `year` (big endian, 16-bit unsigned integer),
    `month` (1 byte), and `day` (1 byte) into a `datetime.date`.
    """
    (year, month, day) = struct.unpack("!HBB", packed)
    return datetime.date(year, month, day)


def pack_datetime(dt):
    """
    Packs a datetime (assumed to be UTC) as a struct with of 16-bit, unsigned `year`
    (big endian), 1 byte `month`, and 1 byte `day`, 1 byte `hour`, 1 byte `minute`,
    and 1 byte `second`.
    """
    midnight = datetime.datetime.combine(dt, datetime.time.min)
    delta = dt - midnight
    return struct.pack("!HBBBBB", dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)


def unpack_datetime(packed):
    """
    Unpacks a 'naive' date + time (no timezone, assume UTC) packed as `year`
    (big endian, 16-bit unsigned integer), `month` (1 byte), `day` (1 byte),
    `hour` (1 byte), `minute` (1 byte), and `second` (1 byte) and returns it as a
    `datetime.datetime` (with `tzinfo = None`, once again, assume UTC).
    """
    (year, month, day, hour, minute, second) = struct.unpack("!HBBBBB", packed)
    return datetime.datetime(year, month, day, hour, minute, second)


def default(obj):
    if isinstance(obj, datetime.datetime):
        return ExtType(EXT_CODE_DATETIME, pack_datetime(obj))
    elif isinstance(obj, datetime.date):
        return ExtType(EXT_CODE_DATE, pack_date(obj))
    else:
        raise TypeError("Unknown type: %r" % (obj,))


def ext_hook(code, data):
    if code == EXT_CODE_DATE:
        return unpack_date(data)
    if code == EXT_CODE_DATETIME:
        return unpack_datetime(data)
    if code == -1:
        if len(data) == 4:
            secs = int.from_bytes(data, byteorder='big', signed=True)
            nsecs = 0
        elif len(data) == 8:
            data = int.from_bytes(data, byteorder='big', signed=False)
            secs = data & 0x00000003ffffffff
            nsecs = data >> 34
        elif len(data) == 12:
            nsecs, secs = struct.unpack('!Iq', data)
        else:
            raise AssertionError("Not reached")

        return datetime.datetime.utcfromtimestamp(secs + nsecs / 1e9)
    # else try to return the original code and data as an ExtType
    return ExtType(code, data)
