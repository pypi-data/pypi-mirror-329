# -*- coding: utf-8 -*-
"""
Test the tests.commons module
"""

from unittest import TestCase, expectedFailure

from . import commons


class FileCache(TestCase):
    """FileCache class test(s)"""

    @expectedFailure
    def test_checksum_error(self):
        """SHA256 checksum mismatch"""
        cache = commons.FileCache(commons.WRONG_CHECKSUM)
        # AssertionError due to checksum mismatch in the .raw property
        print(cache.raw)
