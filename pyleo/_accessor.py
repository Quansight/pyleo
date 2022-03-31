from pandas.api.extensions import register_series_accessor


@register_series_accessor('pyleo')
class PyleoAccessor:
    """
    Making paleoclimate functionality available directly in `pandas.Series` objects.

    The methods implemented here will be available to all `pandas.Series` objects
    if this package is installed.

    Examples
    --------
    >>> import pandas
    >>> import pyleo
    >>> data = pandas.Series([1, 2, 3])
    >>> data.pyleo.standardize()
    """
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def standardize(self):
        return (self._obj - self._obj.mean()) / self._obj.std(ddof=0)

    def spectral(self, method, freq_method):
        pass
