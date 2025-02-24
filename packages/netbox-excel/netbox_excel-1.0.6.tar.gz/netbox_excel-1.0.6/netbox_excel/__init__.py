from netbox.plugins import PluginConfig

__version__ = "1.0.6"

class NetboxExcelConfig(PluginConfig):
    name = "netbox_excel"
    verbose_name = "Netbox excel"
    description = "Import object from file excel"
    version = __version__
    author = "ducna"
    author_email = "ducna@hcd.com.vn"
    base_url = "netbox-excel"
    required_settings = []
    default_settings = {"version_info": False}

config = NetboxExcelConfig
