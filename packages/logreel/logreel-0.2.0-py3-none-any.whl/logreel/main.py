import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from logreel.collector.core import Collector
from logreel.exceptions import StartupError
from logreel.logging_config import get_logger, setup_logging
from logreel.routes.health_route import router
from logreel.version import __version__

setup_logging(log_level="DEBUG")
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(fast_api_app: FastAPI):
    """
    Custom FastAPI lifespan context manager.

    This function manages the application's lifecycle, including the initialisation and cleanup of critical resources
    like the 'Collector' instance. Throughout the all application, there's only one singleton instance of 'Collector'.
    It is used to define setup and teardown tasks that are executed by the 'Collector' at the application
    startup and shutdown, respectively.

    Args:
         fast_api_app (FastAPI): The FastAPI application instance

    Yields:
        None: Yields control back to FastAPI to run its event loop while maintaining the setup resources.

    Lifecycle:
        - **Startup**:
            - Instantiates and initialises the 'Collector' instance.
            - Calls 'coll_start' to perform the async create_task that runs in the background of the FastAPI application.

        -**Shutdown**:
            - Calls 'coll_stop' to clean up resources and shutdown the background tasks.
    """
    logger.info(f"LogReel version {__version__} is starting.")
    coll_ = Collector()
    await coll_.start()

    yield  # Control is handed back to the FastAPI application

    await coll_.stop()
    logger.info("The application shutdown")


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)
app.include_router(router)


def main():
    config = uvicorn.Config(
        app=app, host="0.0.0.0", port=8080, log_level="info", log_config=None
    )
    server = uvicorn.Server(config=config)

    try:
        # Check if the plugins are correctly instantiated and works before starting the server
        coll: Collector = Collector()
        health = coll.check_plugins_health()
        if health.status == "error":
            raise StartupError(health.HealthResponseErrors.last_message)

        if coll:
            server.run()
        else:
            sys.exit(1)

    except KeyError as env_var_exc:
        logger.error(
            "An error occurred while initialising the Collector",
            traceback=env_var_exc,
        )
    except StartupError as startup_exc:
        logger.error("Startup error", traceback=startup_exc)
    except Exception as exc:
        logger.error("An error occurred while running the application", traceback=exc)
    finally:
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
