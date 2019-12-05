#!/usr/bin/env python
"""
Tests for `msgpack_ext` package.
"""
import pytest

import datetime
from msgpack_ext import msgpack_ext, packb, unpackb


def test_pack_date():
    """
    Test for msgpack_ext.pack_date
    """
    date = datetime.date(2008, 8, 16)
    assert b'\x07\xd8\x08\x10' == msgpack_ext.pack_date(date)


def test_unpack_date():
    """
    Test for msgpack_ext.unpack_date
    """
    date = msgpack_ext.unpack_date(b''.fromhex("07D80810"))
    assert datetime.date(2008, 8, 16) == date


def test_pack_datetime():
    """
    Test for msgpack_ext.pack_datetime
    """
    dt = datetime.datetime(1879, 3, 14, 11, 30, 00)
    assert b'\x07W\x03\x0e\xa1\xb8' == msgpack_ext.pack_datetime(dt)


def test_unpack_datetime():
    """
    Test for msgpack_ext.unpack_datetime
    """
    dt = msgpack_ext.unpack_datetime(b''.fromhex("0757030EA1B8"))
    assert datetime.datetime(1879, 3, 14, 11, 30, 00) == dt


def test_packb():
    """
    Test for msgpack_ext.packb
    """
    date = datetime.date(2008, 8, 16)
    assert b'\xd6e\x07\xd8\x08\x10' == packb(date)
    dt = datetime.datetime(1879, 3, 14, 11, 30, 00)
    assert b'\xc7\x06f\x07W\x03\x0e\xa1\xb8' == packb(dt)


def test_unpackb():
    """
    Test for msgpack_ext.unpackb
    """
    date = unpackb(b''.fromhex("D66507D80810"))
    assert datetime.date(2008, 8, 16) == date
    dt = unpackb(b''.fromhex("C706660757030EA1B8"))
    assert datetime.datetime(1879, 3, 14, 11, 30, 00) == dt
