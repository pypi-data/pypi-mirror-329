import asyncio
from datetime import datetime
from functools import wraps

from logreel.logging_config import get_logger
from logreel.models import (
    HealthResponse,
    HealthResponseErrors,
    HealthResponsePlugins,
    PluginHealth,
)
from logreel.plugins.factory import get_plugin
from logreel.settings import settings

logger = get_logger(__name__)


class Collector:
    """
    A singleton class responsible for managing plugins and background tasks.

    The 'Collector' class provides a central interface for initialising, starting, and stopping plugins and background
    tasks. It uses the singleton pattern to ensure a single instance exists throughout the application lifecycle.
    """

    _instance = None

    def __new__(cls):
        """
        Create or return the singleton instance of the Collector.

        This method ensures that only one instance of the Collector class exists.

        Returns:
            Collector: The singleton instance of the Collector class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialise the Collector instance.

        This method sets up the Collector's internal state, including the plugin dictionary, health response model, and
        background task placeholder. The initialisation only occurs once for the singleton instance, thanks to the flag
        self._is_initialised = True.
        """
        if hasattr(self, "_is_initialised") and self._is_initialised:
            return  # Avoid reinitialising

        self.task = None
        self.plugins = {}
        self.get_plugins()
        self.health = self._init_health_response_model()
        self._is_running = False
        self._is_initialised = True

    async def start(self):
        """
        Start the Collector, including all plugins and the background task.

        This method initialises and starts plugins, validates their health, and creates a background task to manage
        ongoing operations.

        Raises:
            RuntimeError: If the Collector fails due to critical issues.
        """
        self.task = asyncio.create_task(self._run(), name="Core._run")
        self._is_running = True

    async def stop(self):
        """
        Stop the Collector, including all plugins and the background task.

        This method gracefully shuts down plugins and waits until the termination of the background task before
        terminating the whole application.
        """
        self._is_running = False
        await self.task

    @staticmethod
    def _init_health_response_model() -> HealthResponse:
        """
        Initialise the application's health response model.

        This static method creates and returns a default 'HealthResponse' model to represent the application's health
        status.

        Returns:
             HealthResponse: The initialised health response model.
        """
        return HealthResponse(
            status="ok",
            startup_timestamp=datetime.now().strftime("%Y%m%d_%H%M%S"),
            last_run_latency="",
            last_run_timestamp="",
            HealthResponsePlugins=HealthResponsePlugins(
                source=PluginHealth(status="ok", details=""),
                destination=PluginHealth(status="ok", details=""),
            ),
            HealthResponseErrors=HealthResponseErrors(
                total_errors=0, last_message="", last_error_time=""
            ),
        )

    def get_plugins(self) -> None:
        """
        Load and initialise source and destination plugins.

        This method uses factory methods to dynamically load and initialise plugins based on the configuration specified
         in the application settings. The loaded plugins are stored in the 'self.plugins' dictionary with the keys
         "source" and "destination".

         Raises:
             PluginNotFoundError: If the specified plugin cannot be found in the respective group.

        Side Effects:
            Updates the 'self.plugins' dictionary with the initialised "source" and "destination" plugins.
        """
        # When adding a new plugin, remember to build the package 'poetry build' and run again 'poetry install --no-dev'
        self.plugins = {
            "source": get_plugin(
                plugin_name=settings.source_plugin, plugin_group="logreel.sources"
            ),
            "destination": get_plugin(
                plugin_name=settings.destination_plugin,
                plugin_group="logreel.destinations",
            ),
        }
        logger.info(f"Plugins '{self.plugins}' loaded successfully")

    def _keep_running(self) -> bool:
        """
        Allow the decorator to run until the stop method has been called.

        This method simulate an infinite loop but with the advantage of terminating it when stop() is called, and It
        will also give more granularity when a specific retry mechanism will be implemented.

        Returns:
            True if the program has not been interrupted by the user.
        """
        if self._is_running:
            return True
        return False

    @staticmethod
    def _retry_if_not_healthy(func):
        """
        A private decorator that continuously checks plugin health, retries upon failure, and only calls 'func' when
        healthy.
        """

        @wraps(func)
        async def wrapper(
            self, retry_delay: int = 4
        ):  # TODO: Implement a specific retry mechanism!
            while self._keep_running():
                try:
                    if (
                        not self.check_plugins_health().status == "ok"
                    ):  # Check the health the Collector and all the plugins
                        logger.error("Waiting to retry due to unhealthy plugins")
                        await asyncio.sleep(delay=retry_delay)
                        continue

                    logger.info("All the plugins are healthy. Running the main logic")
                    await func(self)  # If healthy, call the actual wrapped method

                except Exception as run_exc:
                    logger.error(
                        "An error occurred while in the Collector's run method",
                        traceback=run_exc,
                    )
                    await asyncio.sleep(delay=retry_delay)

                logger.debug(
                    "Waiting to retrieve the next logs after the interval is ended"
                )
                if self._is_running:
                    await asyncio.sleep(delay=settings.interval_seconds)

        return wrapper

    @_retry_if_not_healthy
    async def _run(self) -> None:
        """
        Execute the main logic after verifying plugin health, retrying on failure.

        It gets the previous cursor if any, otherwise returns None. Fetch data from the source and return a new cursor.
        Then, it uploads the data and the new cursor to the destination, and it updates the timestamps.
        This method is decorated with '_retry_health_check', which continuously checks plugin health and only invokes
        this method when the status is "ok". If the plugin is unhealthy or an exception occurs, the method will retry
        after 'retry_delay' seconds.

        Returns:
            None: This method runs indefinitely and does not return a value.

        Raises:
            Exception: Propagates any uncaught exception encountered during execution. Note that the decorator handles
            exceptions by logging them, sleeping for 'retry_delay' seconds, and retrying indefinitely.
        """
        logger.info("Executing the Collector run method")

        prev_cursor: str | None = self.plugins["destination"].get_prev_cursor()
        logger.debug(f"Retrieved previous cursor: {prev_cursor}")

        data, new_cursor = self.plugins["source"].fetch_data_and_new_cursor(
            prev_cursor=prev_cursor
        )
        logger.debug(f"Data fetched: {data}")

        self.plugins["destination"].upload_data_and_new_cursor(
            data=data, new_cursor=new_cursor
        )

        if self.health.last_run_timestamp:
            _last_run_datetime = datetime.strptime(
                self.health.last_run_timestamp, "%Y%m%d_%H%M%S"
            )
            self.health.last_run_latency = str(datetime.now() - _last_run_datetime)
        self.health.last_run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def check_plugins_health(self) -> HealthResponse:
        """
        Check the health of all the plugins and generate a comprehensive health report.

        This method evaluates the health of all configured plugins (e.g., source and destination), calculates relevant
        metrics, and complies the results into a 'HealthResponse' object.

        Returns:
            HealthResponse: A detailed health report containing the status, timestamps, plugin health, and error metrics.

        Raises:
            Exception: If the health check encounters an unexpected failure.
        """
        self.health.status = "ok"  # General plugins health

        for name, plugin in self.plugins.items():
            status, details = plugin.check_plugin_health()
            plugin_health: PluginHealth = getattr(
                self.health.HealthResponsePlugins, name
            )

            if status == "error":
                error_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.health.HealthResponseErrors.total_errors += 1
                self.health.HealthResponseErrors.last_message = details
                self.health.HealthResponseErrors.last_error_time = error_timestamp
                self.health.status = "error"  # General plugins health
                logger.error(f"Plugin: {name}, is unhealthy")

            plugin_health.status = status  # Specific plugin health
            plugin_health.details = details
            setattr(self.health.HealthResponsePlugins, name, plugin_health)

        return self.health
