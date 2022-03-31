import datetime

import pandas
import pyleo  # noqa F401: Loading dtypes and accessors


def test_kyrbp_to_epoch_days():
    expected = (datetime.datetime(2020, 1, 1) - datetime.datetime(1970, 1, 1)).days
    assert pyleo.PyleoDatetimeArray._kyrbp_to_epoch_days(0) == expected


def test_dtype():
    dtype = pyleo.PyleoDatetimeDType(format='kyr BP')

    assert isinstance(dtype, pandas.core.dtypes.base.ExtensionDtype)
    assert dtype.name == 'pyleo_dt'
    assert dtype.format == 'kyr BP'


def test_create_series():
    data = pandas.Series([.04, .0299, .02],
                         #  dtype='pyleo_dt[kyr BP]')
                         dtype=pyleo.PyleoDatetimeDType(format='kyr BP'))

    assert isinstance(data, pandas.Series)
    assert data.dtype.name == 'pyleo_dt'
    assert data.dtype.format == 'kyr BP'

    expected = pandas.Series([1980, 1990, 2000])
    pandas.testing.assert_series_equal(data.dt.year, expected)


def test_standardize():
    series = pandas.Series([1., 2., 3.])

    result = series.pyleo.standardize()

    assert isinstance(result, pandas.Series)

    expected = pandas.Series([-1.224745, 0, 1.224745])
    pandas.testing.assert_series_equal(result, expected)
