import pytest
import pandas as pd
from dtcoords import datetime_coords, DatetimeLike
import numpy as np

@pytest.fixture
def t1():
    return pd.Timestamp.now()

@pytest.fixture
def t2(t1):
    return t1 + pd.DateOffset(hours=2)

@pytest.fixture
def x1():
    return 100

@pytest.fixture
def x2(x1):
    return x1 + 200

class TestDecoratorClass:
    def test_datetime_cast(self, t1, t2):
        """simple test to test basic capability of converting a datetime-like input to numeric."""

        @datetime_coords
        def show_time(t: DatetimeLike, **kwargs):
            return t

        t_float = show_time(t2, _ref=t1)

        assert isinstance(t_float, float)
        assert not np.isnan(t_float)

    def test_avg_velocity(self, t1, t2, x1, x2):
        """more advanced test involving a single computation of multiple datetime-like input.
        Time given in standart `us` numpy time unit. (converting to `h` time unit.)"""

        @datetime_coords
        def compute_avg_velocity(x1, t1: DatetimeLike, x2, t2:DatetimeLike, **kwargs):
            avg = (x2 - x1) / (t2 - t1)
            return avg

        avg_vel_comp = compute_avg_velocity(x1, t1, x2, t2, _unit='h')
        assert np.isclose(avg_vel_comp, 100)

    def test_elapsed_time_comparison(self):
        t1 = np.datetime64(10, 'm')
        t2 = np.datetime64(500, 's')

        @datetime_coords
        def compare_datetime(t1: DatetimeLike, t2: DatetimeLike, _unit=None):
            return t1 > t2

        assert compare_datetime(t1, t2, _unit='ms')

