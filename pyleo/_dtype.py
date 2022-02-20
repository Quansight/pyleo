from pandas.core.dtypes.dtypes import register_extension_dtype, PandasExtensionDtype


@register_extension_dtype
class PyleoType(PandasExtensionDtype):
    pass
