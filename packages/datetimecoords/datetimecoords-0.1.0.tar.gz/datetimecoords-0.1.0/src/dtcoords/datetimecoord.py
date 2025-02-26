from collections import ChainMap
from datetime import datetime
from functools import wraps
from inspect import signature
from typing import Callable, Union, get_args, get_type_hints

import numpy as np
from pandas import Timestamp

DatetimeLike = Union[np.datetime64, datetime, Timestamp]


class DateTimeCoord:
    """class to work on function arguments to convert datetime-like parameters
    into a time reference frame suitable for numeric computations."""

    _UNIT_DEFAULT = "ms"
    _REF_DEFAULT = 1
    _valid_classes = get_args(DatetimeLike)

    def __init__(self, func: Callable = None, ref=None, unit=None):
        self.func = func
        self.ref = ref or self._REF_DEFAULT
        self.unit = unit or self._UNIT_DEFAULT

    def update_reference_frame(self, ref, unit):
        """update instance parameter *ref* and *unit*"""

        self.ref = ref
        self.unit = unit

    def elapsed_time(self, current: DatetimeLike) -> float:
        """compute the elapsed time between event *current* time and *ref* time
        in numeric value."""

        current_dt = np.datetime64(current)
        current_unit = np.datetime_data(current_dt)
        ref_dt = np.datetime64(self.ref, current_unit)
        delta = current_dt - ref_dt
        rate = self._calc_rate(ref_dt, self.unit)

        return delta.astype(float) * rate

    @staticmethod
    def _calc_rate(arr: np.datetime64, unit: str) -> float:
        def native_float(arr):
            return arr.astype(float).item()

        arr_unit = np.datetime_data(arr)
        target_unit = unit
        ref_arr = np.datetime64(1, arr_unit)
        tar_arr = np.datetime64(1, target_unit)

        if native_float(ref_arr.astype(tar_arr.dtype)):
            p1 = native_float(ref_arr.astype(tar_arr.dtype))
            p2 = native_float(tar_arr)
        else:
            p2 = native_float(tar_arr.astype(ref_arr.dtype))
            p1 = native_float(tar_arr)

        rate = p1 / p2
        return rate

    def _process_func_params(self, args, kwargs):
        # collecting func arguments
        sig = signature(self.func)
        annots = get_type_hints(self.func)
        bargs = sig.bind(*args, **kwargs)
        all_params = ChainMap(bargs.arguments, bargs.kwargs)

        # treatment on datetime-like arguments
        annots_dt_only = filter(lambda item: _check_valid_type(item[1]), annots.items())
        dt_params, _ = zip(*annots_dt_only)
        dt_params_x = map(lambda p: (p, self.elapsed_time(all_params[p])), dt_params)
        call_params = all_params.new_child(dict(dt_params_x))
        binded_params = sig.bind(**dict(call_params))
        return binded_params.args, binded_params.kwargs

    def __call__(self, *args, **kwargs):
        if any(kw in kwargs for kw in ("_ref", "_unit")):
            # setting up instance due to args and kwargs
            ref = kwargs.pop("_ref", self.ref)
            unit = kwargs.pop("_unit", self.unit)
            self.update_reference_frame(ref=ref, unit=unit)
            args, kwargs = self._process_func_params(args, kwargs)
            return args, kwargs
        else:
            args, kwargs = self._process_func_params(args, kwargs)
            return self.func(*args, **kwargs)


def _check_valid_type(typ):
    """typechecker for Unions"""

    valid_classes = get_args(DatetimeLike)
    try:
        return any(
            issubclass(class_item, valid_classes) for class_item in get_args(typ)
        )
    except TypeError:
        return False


def datetime_coords(func: Callable):
    """function decorator to locate transform datetime-like arguments
    into a time reference frame."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        args, kwargs = datetime_coord(*args, **kwargs)
        return func(*args, **kwargs)

    datetime_coord = DateTimeCoord(func)

    return wrapper


__all__ = ["datetime_coords", "DatetimeLike"]
