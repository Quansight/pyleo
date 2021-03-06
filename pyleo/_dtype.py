import re

from pandas._libs.tslibs import Timestamp
from pandas.core.dtypes.dtypes import register_extension_dtype, PandasExtensionDtype


@register_extension_dtype
class PyleoDatetimeDType(PandasExtensionDtype):
    name = 'pyleo_dt'
    kind = 'M'
    type = Timestamp
    _known_formats = 'kyr BP',

    # TODO Using the name `format` here which refers to pyleoclim unit, (something like "kyr BP",
    # thousands of years since present time), since `unit` is the original DatetimeTZDtype
    # `unit='ns'` of datetimes. Not sure if there is a better name.
    def __init__(self, format):
        if format not in self._known_formats:
            raise ValueError(f'pyleo_dt format "{format}" not understood. '
                             f'Use one of {self._known_formats}')
        self._format = format

    @property
    def format(self):
        return self._format

    @classmethod
    def construct_array_type(cls):
        from ._array import PyleoDatetimeArray
        return PyleoDatetimeArray

    @classmethod
    def construct_from_string(cls, string):
        match = re.search(r'^pyleo_dt\[(.*)\]$', string)
        if not match:
            raise TypeError(f"Cannot construct a '{cls.__name__}' from '{string}'")
        format = match.group(1)
        if format != 'kyr BP':
            raise ValueError(f'Unknown format {format}')
        return cls(format=format)
