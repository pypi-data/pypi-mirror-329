from uuid import UUID

from pydantic import ConfigDict, BaseModel


class UniAnswerParams(BaseModel):
    topic: str
    id: UUID
    ttl_s: int

    model_config = ConfigDict(
        frozen=True,
        extra="ignore",
    )
