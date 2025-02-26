import typing as t
from importlib.metadata import entry_points

from logreel.exceptions import PluginNotLoadedError
from logreel.logging_config import get_logger

logger = get_logger(__name__)


def get_plugin[T](plugin_name: str, plugin_group: str) -> t.Type[T]:
    """
    Retrieve a plugin by name and group.

    This function searches for an entry point matching the specific plugin name and group.
    If the plugin cannot be loaded, it raises a PluginNotFoundError with detailed context.

    Args:
         plugin_name (str): The name of the plugin to retrieve.
         plugin_group (str): The group under which the plugin is registered.

    Returns:
        Type[T]: The plugin class.

    Raises:
        PluginNotFoundError: If the plugin cannot be found or loaded.
    """
    try:
        plugin_names = [plugin.name for plugin in entry_points(group=plugin_group)]
        logger.debug(f"Discovered {len(plugin_names)} plugins: {plugin_names}")

        for entry_point in entry_points(group=plugin_group, name=plugin_name):
            if entry_point.name == plugin_name:
                logger.debug(
                    f"The plugin '{plugin_name}' match the name of one of the available plugins."
                )

                loaded_entry_point = entry_point.load()
                logger.debug(
                    f"The plugin '{plugin_name}' has been loaded correctly."
                )

                instantiated_entry_point = loaded_entry_point()
                logger.debug(
                    f"The plugin '{plugin_name}' has been instantiated correctly."
                )
                return instantiated_entry_point  # Returning the instantiation of the entry point

        raise IndexError(
            f"The plugin '{plugin_name}' is not listed in group '{plugin_group}'."
        )

    except (
        IndexError,
        ModuleNotFoundError,
        AttributeError,
        FileNotFoundError,
    ) as original_plugin_exc:
        logger.error(
            "An error occurred during the plugin discovery",
            traceback=original_plugin_exc,
            plugin_name=plugin_name,
        )
        raise PluginNotLoadedError(
            plugin_name=plugin_name,
            message=f"Error while loading plugin '{plugin_name}' from group '{plugin_group}'.",
            cause=original_plugin_exc,
        )
