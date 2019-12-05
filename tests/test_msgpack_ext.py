#!/usr/bin/env python
"""
Tests for `msgpack_ext` package.
"""
import pytest

import datetime
from msgpack_ext import msgpack_ext, unpackb


def test_unpack_date():
    """
    Test for msgpack_ext.unpack_date
    """
    date = msgpack_ext.unpack_date(b''.fromhex("07D80810"))
    assert datetime.date(2008, 8, 16) == date


def test_unpack_datetime():
    """
    Test for msgpack_ext.unpack_datetime
    """
    dt = msgpack_ext.unpack_datetime(b''.fromhex("0757030EA1B8"))
    assert datetime.datetime(1879, 3, 14, 11, 30, 00) == dt


def test_unpackb():
    """
    Test for msgpack_ext.unpackb
    """
    date = unpackb(b''.fromhex("D66507D80810"))
    assert datetime.date(2008, 8, 16) == date
    dt = unpackb(b''.fromhex("C706660757030EA1B8"))
    assert datetime.datetime(1879, 3, 14, 11, 30, 00) == dt
