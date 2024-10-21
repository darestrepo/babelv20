from importlib import import_module
from .platform_adapter import PlatformAdapter


def get_adapter(adapter_name: str) -> PlatformAdapter:
    """
    Get the appropriate adapter instance based on the adapter name.

    Args:
        adapter_name (str): The name of the adapter to retrieve.

    Returns:
        PlatformAdapter: An instance of the adapter.

    Raises:
        ValueError: If the adapter is not found or cannot be imported.
    """
    try:
        module_name = f"app.api.adapters.{adapter_name}_adapter"
        module = import_module(module_name)
        adapter_class_name = f"{adapter_name.capitalize()}Adapter"
        adapter_class = getattr(module, adapter_class_name)
        adapter_instance = adapter_class()
        
        return adapter_instance
    except ImportError as e:
        raise ValueError(f"Adapter module {adapter_name} not found. Check if the file exists and is in the correct location.") from e
    except AttributeError as e:
        raise ValueError(f"Adapter class {adapter_name.capitalize()}Adapter not found in module.") from e
    except Exception as e:
        raise ValueError(f"Unexpected error occurred while getting adapter {adapter_name}.") from e

# Usage in scala360_controller.py
# adapter = get_adapter("scala360")
# print(f"Adapter: {adapter}")
