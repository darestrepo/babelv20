from importlib import import_module
from .platform_adapter import PlatformAdapter

class AdapterFactory:
    @staticmethod
    def get_adapter(platform: str) -> PlatformAdapter:
        try:
            module_name = f"app.api.adapters.{platform}_adapter"
            module = import_module(module_name)
            adapter_class = getattr(module, f"{platform.capitalize()}Adapter")
            return adapter_class()
        except (ImportError, AttributeError):
            raise ValueError(f"Unsupported platform: {platform}")
