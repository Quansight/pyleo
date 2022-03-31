import datetime

import pandas
from pandas.core.arrays import DatetimeArray
from pandas._libs.arrays import NDArrayBacked


class PyleoDatetimeArray(DatetimeArray):
    """
    A regular pandas datetime column, but contains the unit.

    Internally, the information will be stored using second precision
    (when implemented) with a certain epoch, but for the interactions
    with the user, this date will be presented given a specific unit
    (for example, thousands of years before present time, "kyr BP").

    Examples
    --------
    >>> import pandas
    >>> import pyleo
    >>> data = pandas.Series([38.37379, 503.05731, 798.90051],
    ...                      dtype='pyleo_dt[kyr BP]')
    """
    def __init__(self, values):
        # Converting from thousands of years to days, the minimum unit supported by `to_datetime`
        # TODO this implementation is based on the 1970 epoch, not based in present date, which
        # is not yet implemented
        values = pandas.to_datetime([self._kyrbp_to_epoch_days(v) for v in values], unit='D')
        NDArrayBacked.__init__(self, values=values.values, dtype=self.dtype)

    @staticmethod
    def _kyrbp_to_epoch_days(value):
        """
        Convert from thousands of years since present time to number of days since 1970 epoch.
        """
        years_since_present_time = value * 1000
        days_since_present_time = years_since_present_time * 365.25
        # XXX not sure if there is a convention, this should be dynamic, or what
        present_time = datetime.datetime(2020, 1, 1)
        regular_date = present_time - datetime.timedelta(days=days_since_present_time)
        days_after_epoch = (regular_date - datetime.datetime(1970, 1, 1)).days
        return days_after_epoch

    @property
    def dtype(self):
        from ._dtype import PyleoDatetimeDType
        return PyleoDatetimeDType(format='kyr BP')

    @classmethod
    def _from_sequence(cls, values, dtype=None, copy=True):
        return cls(values)
