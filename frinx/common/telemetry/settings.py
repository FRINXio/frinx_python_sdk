from pydantic import BaseModel
from pydantic import Field


class MetricsSettings(BaseModel):
    metrics_enabled: bool = True
    port: int = Field(default=8000)
