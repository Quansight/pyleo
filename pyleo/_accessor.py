from pandas.api.extensions import register_series_accessor


@register_series_accessor('pyleo')
class PyleoAccessor:
    pass
