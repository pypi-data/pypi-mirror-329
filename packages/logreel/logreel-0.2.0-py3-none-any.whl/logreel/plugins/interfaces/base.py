import os
from abc import ABC, abstractmethod

from logreel.models import PluginHealthResponse


class BasePlugin(ABC):
    """
    Abstract Base class for Plugins.

    This class provides a common interface for all plugins, defining the methods that subclasses must implement and
    a utility method available to all plugins.
    """

    @abstractmethod
    def check_plugin_health(self) -> PluginHealthResponse:  # pragma: no cover
        """
        Check the health of the plugin.

        This method performs health checks specific to the plugin implementation and returns the health status and
        optional details.

        Returns:
            PluginHealthResponse: A tuple containing:
                - str: The health status, either "ok" or "error".
                - Optional[str]: Additional details about the health check, or None if no details are available.
        """
        ...

    def get_env_var(self, var_name: str, default: str | None = None) -> str | KeyError:
        """
        Retrieve an environment variable's value.

        This utility method fetches the value of a specific environment variable. If the variable is not found and no
        default value is provided, it raises a KeyError.

        Args:
            var_name (str): The name of the environment to retrieve.
            default (Optional[str]): A default value to return if the variable is not set. If None, a KeyError is raised
            for missing variables.

        ReturnS:
            str: The value of the environment variable.

        Raises:
            KeyError: If the environment variable is not found and no default value is provided.
        """
        var = os.getenv(key=var_name, default=default)
        if not var:
            raise KeyError(f"{var_name}")
        return var
