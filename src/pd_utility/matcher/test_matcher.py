from __future__ import absolute_import
from unittest import TestCase
import matcher

__author__ = "Francis Ilechukwu"
__project__ = "Python Dance"


class TestMatcher(TestCase):
    def test_is_match(self):
        self.assertTrue(matcher.is_match({"a": 1, "b": 2, "c": 3, "d": 4}, {"a": 1, "b": 2, "c": 3, "d": 4}))
        self.assertFalse(matcher.is_match({"a": 1, "g": 2, "c": 3, "d": 4}, {"r": 1, "b": 2, "c": 3, "d": 4}))
        self.assertFalse(matcher.is_match({"a": 1, "b": 3, "c": 3, "d": 4}, {"a": 1, "b": 2, "c": 3, "d": 4}))
        self.assertFalse(matcher.is_match({"a": 1, "b": [5, 6, 7], "c": 3, "d": 4}, {"a": 1, "b": 2, "c": 3, "d": 4}))
        self.assertTrue(matcher.is_match({"a": 1, "b": [5, 6, 7], "c": 3, "d": 4}, {"a": 1, "b": [5, 6, 7], "c": 3,
                                                                                    "d": 4}))
        self.assertFalse(matcher.is_match({"a": 1, "b": [5, 6, 7], "c": 3, "d": 4}, {"a": 1, "b": [7, 8, 9], "c": 3,
                                                                                     "d": 4}))
        self.assertTrue(matcher.is_match({"a": 1, "b": [5, 6, 7], "c": 3, "d": 4}, {"a": 1, "b": [7, 5, 6], "c": 3,
                                                                                    "d": 4}))
        self.assertTrue(
            matcher.is_match({"a": 1, "b": [5, 6, 7], "c": 3, "d": 4}, {"a": 1, "b": [7, 5, 6], "c": 3, "d": 4,
                                                                        "e": 5}))
        self.assertFalse(
            matcher.is_match({"a": 1, "b": [5, 6, 7], "c": 3, "d": 4, "e": 5}, {"a": 1, "b": [7, 5, 6], "c": 3,
                                                                                "d": 4}))
        self.assertTrue(matcher.is_match({"a": 1, "b": {"a": 45, "b": "impeccable"}, "c": 3, "d": 4}, {"a": 1, "b":
            {"a": 45, "b": "impeccable"}, "c": 3,  "d": 4}))
        self.assertFalse(matcher.is_match({"a": 1, "b": {"a": 45, "b": "impeccable"}, "c": 3, "d": 4}, {"a": 1, "b":
            {"a": 45, "b": "jack"}, "c": 3, "d": 4}))
