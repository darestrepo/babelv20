from importlib import import_module


def get_controller(controller_name: str):
    """
    Get the appropriate controller instance based on the controller name.

    Args:
        controller_name (str): The name of the controller to retrieve.

    Returns:
        Controller: An instance of the controller.

    Raises:
        ValueError: If the controller is not found or cannot be imported.
    """
    try:
        module_name = f"app.api.controllers.{controller_name}_controller"
        module = import_module(module_name)
        function_name = f"process_return_message"
        function = getattr(module, function_name)
        
        return function
    except ImportError as e:
        raise ValueError(f"Controller module {controller_name} not found. Check if the file exists and is in the correct location.") from e
    except AttributeError as e:
        raise ValueError(f"Controller class {controller_name.capitalize()}Controller not found in module.") from e
    except Exception as e:
        raise ValueError(f"Unexpected error occurred while getting controller {controller_name}.") from e

