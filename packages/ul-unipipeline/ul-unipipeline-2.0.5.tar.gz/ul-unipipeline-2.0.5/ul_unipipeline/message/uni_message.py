from pydantic import ConfigDict, BaseModel


class UniMessage(BaseModel):
    model_config = ConfigDict(extra="ignore")
