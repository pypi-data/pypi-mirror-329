import typing as t

from pydantic import BaseModel

PluginHealthResponse = t.Tuple[t.Literal["ok", "error"], str | None]


class PluginHealth(BaseModel):
    status: t.Literal["ok", "error"]
    details: t.Optional[str]


class HealthResponseErrors(BaseModel):
    total_errors: int
    last_message: str
    last_error_time: str


class HealthResponsePlugins(BaseModel):
    source: PluginHealth
    destination: PluginHealth


class HealthResponse(BaseModel):
    status: t.Literal["ok", "error"]
    startup_timestamp: str
    last_run_latency: str
    last_run_timestamp: str
    HealthResponsePlugins: HealthResponsePlugins
    HealthResponseErrors: HealthResponseErrors
