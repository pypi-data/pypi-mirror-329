import typing as t
from typing import Optional


class PluginNotLoadedError(Exception):
    """
    Custom exception raised when a plugin cannot be loaded.

    This exception is used to encapsulate all errors related to plugin discovery, loading, or initialisation.
    It provides the plugin name and a dedicated error message.
    """

    def __init__(
        self,
        plugin_name: str,
        message: t.Optional[str] = None,
        cause: Optional[Exception] = None,
    ):
        """
        Initialise the PluginNotFoundError.

        Args:
            plugin_name (str): The name of the plugin that could not be loaded.
            message (Optional[str]): A detailed message describing the error. Defaults to None.
            cause (Optional[Exception]): The original exception that caused the error, if available.
        """

        self.plugin_name = plugin_name
        self.message = message or f"Plugin '{plugin_name}' not found"
        self.cause = cause
        super().__init__(self.message)


class StartupError(Exception):
    """
    Custom exception raised during application startup

    This exception is used to indicate critical issues encountered during the initialisation or startup phase of the
    application. It provides additional context about the startup error.
    """

    pass
