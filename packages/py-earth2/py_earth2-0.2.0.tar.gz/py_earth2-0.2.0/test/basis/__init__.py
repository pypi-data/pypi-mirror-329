from __future__ import annotations

import numpy

numpy.random.seed(0)


def assert_equal(x, y):
    assert x == y


def assert_true(x):
    assert x


def assert_false(x):
    assert not x
