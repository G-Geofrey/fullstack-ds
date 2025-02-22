import importlib
import sys

def import_module(module_name, module_path=None):
    """
    Dynamically imports or reloads a Python module.

    This function attempts to import a module specified by 'module_name'.
    If 'module_path' is provided, it adds the path to the system's module search paths
    before attempting the import. If the module is already loaded, it reloads the module.

    Args:
        module_name: The name of the module to import (e.g., "os", "my_module").
        module_path: Optional. Path to the directory containing the module.

    Returns:
        The imported or reloaded module object, or None if the import fails.

    Raises:
        ImportError: If the module cannot be found or imported.
        Exception: If any other unexpected error occurs during import.

    Example:
        # Import a standard module
        os_module = import_module("os")

        # Import a module from a specific path
        my_module_path = "/path/to/my/modules"
        my_module = import_module("my_module", my_module_path)

        # Reload an already loaded module
        reloaded_os_module = import_module("os")
    """
    original_path = sys.path[:]
    try:
        if module_path:
            sys.path.insert(0, module_path)

        if module_name in sys.modules:
            module = sys.modules[module_name]
            module = importlib.reload(module)
            return module
        else:
            module = importlib.import_module(module_name)
            return module
    except ImportError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occured: {e}")
    finally:
        sys.path = original_path

