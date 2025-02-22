import typing as t
from datetime import datetime

from pydantic import BaseModel, HttpUrl

from tobikodata.http_client.api_models.v1.common import V1Status


class V1Run(BaseModel):
    environment: str
    run_id: str
    start_at: t.Optional[datetime]
    end_at: t.Optional[datetime]
    error_message: t.Optional[str]
    status: V1Status
    link: HttpUrl

    @property
    def complete(self) -> bool:
        return self.status.complete
