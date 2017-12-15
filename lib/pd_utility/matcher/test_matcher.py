from __future__ import absolute_import
from unittest import TestCase
import matcher


__author__ = "Francis Ilechukwu"
__project__ = "Python Dance"


class TestMatcher(TestCase):
    def test_is_match(self):
        self.assertTrue(matcher.is_match({"a": 1, "b": 2, "c": 3, "d": 4}, {"a": 1, "b": 2, "c": 3, "d": 4}))
