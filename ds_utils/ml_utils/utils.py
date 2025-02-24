import importlib
import sys
import logging

from pathlib import Path
from IPython import get_ipython
from datetime import datetime
from enum import Enum

def reset_kernel():
    """Resets the IPython kernel's namespace, clearing all variables and imports.

    This function is only effective within an IPython environment (e.g., Jupyter notebooks).
    """
    ipython = get_ipython()
    if ipython:
        ipython.reset(True)
    else:
        print("Warning: Not running in an IPython environment. Namespace reset skipped.")

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
        if module_path is not None:
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

    
def get_logger(name, log_level=logging.INFO, log_format=None, stream=True, log_file=None, propagate=False):
    """
    Retrieves or creates a logger with the specified configuration.

    This function configures a logger with the given name, log level, format, and output streams (console and/or file).
    It allows for customization of log messages and their destination.

    Args:
        name (str): The name of the logger (typically __name__).
        log_level (int, optional): The logging level (e.g., logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL). Defaults to logging.INFO.
        log_format (str, optional): The format of the log messages. Defaults to "%(asctime)s:%(name)s:%(levelname)s:%(message)s".
        stream (bool, optional): If True, logs will be output to the console (stdout). Defaults to True.
        log_file (str, optional): The path to the log file. If provided, logs will be written to this file. Defaults to None (no file logging).
        propagate (bool, optional): Determines if log messages should propagate to parent loggers. Defaults to False.

    Returns:
        logging.Logger: The configured logger object.

    Example:
        >>> import logging
        >>> logger = get_logger(__name__, log_level=logging.DEBUG, log_file="my_app.log")
        >>> logger.debug("This is a debug message.")
        >>> logger.info("This is an info message.")

    Notes:
        - If 'log_file' is provided, the function ensures that the parent directory exists.
        - The 'logger.handlers = []' line clears any existing handlers, ensuring consistent logging behavior.
        - The date format used in the log messages is "YYYY-MM-DD HH:MM:SS".
        - When stream or log_file is None, the stream handler will be added.
    """

    if log_format is None:
        log_format = "%(asctime)s:%(name)s:%(levelname)s:%(message)s"
    formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # overwrite all handlers if any
    logger.handlers = []

    if stream or log_file is None:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    if log_file is not None:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file.as_posix())
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.propagate = propagate

    return logger

# ==================== Project Defintion ====================

# Enumerations
class TimeFormat(Enum):
    NONE = "none"
    DATE = "date"
    TIME = "datetime"

class ProjectDefinition:
    """
    A class for generating project-related namespace strings.
    """

    def __init__(self, project, version, description=None):
        """
        Initializes the NamespaceHandler.

        Args:
            project (str): The project name.
            version (str): The project version.
            description (str, optional): A description of the project. Defaults to a generated description.
        """
        self._project = project
        self._version = version
        self._description = description

    @property
    def project_namespace(self):
        """
        Returns a dictionary containing project namespace information.
        """
        return {
            "project_name": self.project,
            "project_version": self.version,
            "experiment_name": self.experiment_name,
            "model_name": self.model_name,
        }

    @property
    def project(self):
        """Returns the project name."""
        return self._project

    @project.setter
    def project(self, project_name):
        """Sets the project name."""
        self._project = project_name

    @property
    def version(self):
        """Returns the project version with dots replaced by hyphens."""
        return self._version.replace(".", "-")

    @version.setter
    def version(self, version_name):
        """Sets the project version."""
        self._version = version_name

    @property
    def description(self):
        """Returns the project description, or a default description if none is set."""
        if self._description is None:
            return f"Version {self.version} of {self.project} project"
        else:
            return self._description

    @description.setter
    def description(self, description):
        """Sets the project description."""
        self._description = description

    @property
    def experiment_name(self):
        """Returns the experiment name, generated from the project and version."""
        return f"{self.project}-v{self.version}"

    @property
    def model_name(self):
        """Returns the model name, generated from the experiment name."""
        return f"{self.experiment_name}-model"
    
    def get_run_name(self, name, time_fmt=TimeFormat.NONE):
        """
        Generates a run name with optional date/time stamps.

        Args:
            name (str): The base name for the run.
            time_fmt (TimeFormat, optional): The time format to use. Defaults to TimeFormat.NONE.

        Returns:
            str: The generated run name.

        Raises:
            ValueError: If the time_fmt is not a valid TimeFormat.
        """

        DATE_FORMAT = "%Y-%m-%d"
        TIME_FORMAT = "%Y-%m-%d-%H-%M-%S"

        try:
            time_fmt_enum = TimeFormat(time_fmt)
        except ValueError:
            raise ValueError(f"time_fmt must be one of {[x.value for x in TimeFormat]}")
        
        if time_fmt_enum == TimeFormat.NONE:
            return f"{self.experiment_name}-run-{name}"
        elif time_fmt_enum == TimeFormat.DATE:
            return f"{self.experiment_name}-run-{name}-{datetime.today().strftime(DATE_FORMAT)}"
        else:
            return f"{self.experiment_name}-run-{name}-{datetime.today().strftime(TIME_FORMAT)}"
        

