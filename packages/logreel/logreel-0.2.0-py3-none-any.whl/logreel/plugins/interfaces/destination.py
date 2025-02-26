from abc import abstractmethod

from logreel.plugins.interfaces.base import BasePlugin


class DestinationPlugin(BasePlugin):
    """
    Abstract base class for destination plugins.

    This class defines the interface for destination plugins that manage data storage and cursor updates.
    """

    @abstractmethod
    def get_prev_cursor(self) -> str | None:  # pragma: no cover
        """
        Retrieve the previous cursor for tracking the data state.

        Returns:
             Optional[str]: The previous cursor if available, or None if no cursor exists.
        """
        ...

    @abstractmethod
    def upload_data_and_new_cursor(self, data, cursor: str) -> None:  # pragma: no cover
        """
        Upload data and update the cursor for tracking the data state.

        Args:
             data: The data to be uploaded to the destination
             cursor (str): The new cursor to update in the destination.

        Returns:
            None
        """
        ...
