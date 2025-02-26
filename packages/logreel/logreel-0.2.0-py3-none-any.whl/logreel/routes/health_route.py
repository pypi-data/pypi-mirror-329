from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from logreel.collector.core import Collector
from logreel.logging_config import get_logger
from logreel.models import HealthResponse

router = APIRouter()
logger = get_logger()


@router.get(
    "/health",
    response_model=HealthResponse,
)
async def check_health() -> JSONResponse:
    """
    Endpoint to check the health of all plugins.
    The HealthResponse object containing the status of Collector and all the plugins
    Return:
         200 OK with the HealthResponse model if is_collector_health is True
         503 Service Unavailable with the HealthResponse model if is_collector_health is False
    """
    coll = Collector()
    health = coll.check_plugins_health()

    if health.status == "ok":
        return JSONResponse(content=health.model_dump(), status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(
            content=health.model_dump(), status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
