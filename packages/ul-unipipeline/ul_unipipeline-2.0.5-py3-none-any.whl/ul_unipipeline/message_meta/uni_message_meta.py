import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID

from pydantic import ConfigDict, BaseModel

from ul_unipipeline.answer.uni_answer_params import UniAnswerParams
from ul_unipipeline.message_meta.uni_message_meta_err import UniMessageMetaErr
from ul_unipipeline.message_meta.uni_message_meta_error_topic import UniMessageMetaErrTopic


class UniMessageMeta(BaseModel):
    id: UUID
    date_created: datetime
    payload: Dict[str, Any]

    parent: Optional[Dict[str, Any]] = None
    error: Optional[UniMessageMetaErr] = None

    unwrapped: bool
    answer_params: Optional[UniAnswerParams] = None

    worker_creator: Optional[str] = None  # name of worker who created it

    ttl_s: Optional[int] = None

    model_config = ConfigDict(
        frozen=True,
        extra="ignore",
    )

    @property
    def real_ttl_s(self) -> Optional[int]:
        return self.ttl_s or (self.answer_params.ttl_s if self.answer_params is not None else None)

    @property
    def need_answer(self) -> bool:
        return self.answer_params is not None

    @property
    def has_error(self) -> bool:
        return self.error is not None

    @staticmethod
    def create_new(data: Dict[str, Any], unwrapped: bool, answer_params: Optional[UniAnswerParams] = None, error: Optional[UniMessageMetaErr] = None, ttl_s: Optional[int] = None) -> 'UniMessageMeta':
        return UniMessageMeta(
            id=uuid.uuid4(),
            date_created=datetime.now(),
            payload=data,
            parent=None,
            error=error,
            answer_params=answer_params,
            unwrapped=unwrapped,
            ttl_s=ttl_s,
        )

    def create_child(self, payload: Dict[str, Any], unwrapped: bool, answer_params: Optional[UniAnswerParams] = None, ttl_s: Optional[int] = None) -> 'UniMessageMeta':
        return UniMessageMeta(
            id=uuid.uuid4(),
            date_created=datetime.now(),
            payload=payload,
            parent=self.model_dump(),
            unwrapped=unwrapped,
            answer_params=answer_params,
            error=None,
            ttl_s=ttl_s,
        )

    def create_error_child(self, error_topic: UniMessageMetaErrTopic, error: Exception, ttl_s: Optional[int] = None) -> 'UniMessageMeta':
        return UniMessageMeta(
            id=self.id,
            date_created=self.date_created,
            payload=self.payload,
            parent=self.model_dump(),
            unwrapped=self.unwrapped,
            answer_params=self.answer_params,
            error=UniMessageMetaErr(
                error_topic=error_topic,
                error_type=type(error).__name__,
                error_message=str(error),
                retry_times=self.error.retry_times + 1 if self.error is not None else 0
            ),
            ttl_s=ttl_s,
        )
