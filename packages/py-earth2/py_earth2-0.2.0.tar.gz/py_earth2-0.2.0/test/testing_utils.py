from __future__ import annotations

import importlib
import importlib.util
import os
import sys

# from distutils.version import LooseVersion
from functools import wraps

import pytest
from numpy.testing import assert_almost_equal


def if_environ_has(var_name):
    # Test decorator that skips test if environment variable is not defined
    def if_environ(func):
        @wraps(func)
        def run_test(*args, **kwargs):
            if var_name in os.environ:
                return func(*args, **kwargs)
            else:
                pytest.skip("Only run if %s environment variable is defined." % var_name)

        return run_test

    return if_environ


def if_platform_not_win_32(func):
    @wraps(func)
    def run_test(*args, **kwargs):
        if sys.platform == "win32":
            pytest.skip("Skip for 32 bit Windows platforms.")
        else:
            return func(*args, **kwargs)

    return run_test


# def if_sklearn_version_greater_than_or_equal_to(min_version):
#     """
#     Test decorator that skips test unless sklearn version is greater than or
#     equal to min_version.
#     """

#     def _if_sklearn_version(func):
#         @wraps(func)
#         def run_test(*args, **kwargs):
#             import sklearn

#             if LooseVersion(sklearn.__version__) < LooseVersion(min_version):
#                 pytest.skip("sklearn version less than %s" % str(min_version))
#             else:
#                 return func(*args, **kwargs)

#         return run_test

#     return _if_sklearn_version


def if_statsmodels(func):
    """Test decorator that skips test if statsmodels not installed."""

    @wraps(func)
    def run_test(*args, **kwargs):
        if importlib.util.find_spec("statsmodels") is None:
            pytest.skip("statsmodels not available.")
        else:
            return func(*args, **kwargs)

    return run_test


def if_pandas(func):
    """Test decorator that skips test if pandas not installed."""

    @wraps(func)
    def run_test(*args, **kwargs):
        if importlib.util.find_spec("pandas") is None:
            pytest.skip("pandas not available.")
        else:
            return func(*args, **kwargs)

    return run_test


def if_sympy(func):
    """Test decorator that skips test if sympy not installed"""

    @wraps(func)
    def run_test(*args, **kwargs):
        if importlib.util.find_spec("sympy") is None:
            pytest.skip("sympy not available.")
        else:
            return func(*args, **kwargs)

    return run_test


def if_patsy(func):
    """Test decorator that skips test if patsy not installed."""

    @wraps(func)
    def run_test(*args, **kwargs):
        if importlib.util.find_spec("patsy") is None:
            pytest.skip("patsy not available.")
        else:
            return func(*args, **kwargs)

    return run_test


def assert_list_almost_equal(list1, list2):
    for el1, el2 in zip(list1, list2, strict=False):
        assert_almost_equal(el1, el2)


def assert_list_almost_equal_value(list, value):
    for el in list:
        assert_almost_equal(el, value)
