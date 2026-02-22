"""Pydantic models for DevPulse."""

from pydantic import BaseModel, Field


class LatencyResult(BaseModel):
    """Model for latency test result."""

    url: str
    status_code: int | None = None
    response_time_ms: float | None = None
    error: str | None = None

    @property
    def is_success(self) -> bool:
        """Check if request was successful."""
        return self.status_code is not None and self.error is None


class LatencyStats(BaseModel):
    """Model for aggregated latency statistics."""

    results: list[LatencyResult]
    avg_latency_ms: float
    fastest_ms: float
    slowest_ms: float
    success_count: int
    total_count: int


class CurlRequest(BaseModel):
    """Model for parsed curl request."""

    url: str
    method: str = "GET"
    headers: dict[str, str] = Field(default_factory=dict)
    data: str | None = None
    json_data: dict | None = None


class PortProcess(BaseModel):
    """Model for process using a port."""

    pid: int
    name: str
    port: int
