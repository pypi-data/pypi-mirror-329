from pydantic import ConfigDict, BaseModel

from ul_unipipeline.message_meta.uni_message_meta_error_topic import UniMessageMetaErrTopic


class UniMessageMetaErr(BaseModel):
    error_topic: UniMessageMetaErrTopic
    error_type: str
    error_message: str
    retry_times: int

    model_config = ConfigDict(
        extra="ignore",
        frozen=True,
    )
