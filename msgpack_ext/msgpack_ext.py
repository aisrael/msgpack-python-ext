"""Main module."""

import datetime
import msgpack
import struct


def unpack_date(packed):
    """
    Unpacks a UTC date packed as `year` (big endian, 16-bit unsigned integer),
    `month` (1 byte), and `day` (1 byte) into a `datetime.date`.
    """
    (year, month, day) = struct.unpack("!HBB", packed)
    return datetime.date(year, month, day)


def unpack_datetime(packed):
    """
    Unpacks a 'naive' date + time (no timezone, assume UTC) packed as `year`
    (big endian, 16-bit unsigned integer), `month` (1 byte), `day` (1 byte),
    and `seconds_from_midnight` (16-bit unsigned integer) and returns it as a
    `datetime.datetime` (with `tzinfo = None`, once again, assume UTC).
    """
    date = unpack_date(packed[0:4])
    (seconds_from_midnight,) = struct.unpack("!H", packed[4:])
    return datetime.datetime.combine(date, datetime.time.min) + datetime.timedelta(seconds=seconds_from_midnight)


def ext_hook(code, data):
    if code == 101:
        return unpack_date(data)
    if code == 102:
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
    return msgpack.ExtType(code, data)
