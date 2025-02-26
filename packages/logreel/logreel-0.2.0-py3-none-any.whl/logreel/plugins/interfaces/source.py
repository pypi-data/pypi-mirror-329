import typing as t
from abc import abstractmethod

from logreel.plugins.interfaces.base import BasePlugin


class SourcePlugin(BasePlugin):
    """
    Abstract base class for the source plugins.

    This class defines the interface for source plugins that fetch data and generate new cursors.
    """

    @abstractmethod
    def fetch_data_and_new_cursor(
        self, prev_cursor: str
    ) -> t.Tuple[str, t.Any]:  # pragma: no cover
        """
        Fetch data and generate a new cursor for the next tracking point.

        Args:
            prev_cursor (Optional[str]): The previous cursor used to fetch new data (logs not yet consumed by
            Google SecOps).

        Returns:
            Tuple[str, t.Any]: A tuple containing:
                - str: The cursor for future tracking.
                - Any: The fetched data corresponding to the new cursor.
        """
        ...
