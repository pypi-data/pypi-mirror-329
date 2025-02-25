from pydantic import ConfigDict, BaseModel


class UniDynamicDefinition(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        frozen=True,
    )
