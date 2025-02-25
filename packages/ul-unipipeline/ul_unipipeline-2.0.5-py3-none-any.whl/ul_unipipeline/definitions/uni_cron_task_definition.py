from typing import Optional
from uuid import UUID

from pydantic import model_validator, field_validator
from pydantic_core.core_schema import ValidationInfo

from ul_unipipeline.definitions.uni_definition import UniDefinition
from ul_unipipeline.definitions.uni_worker_definition import UniWorkerDefinition


class UniCronTaskDefinition(UniDefinition):
    id: UUID
    name: str
    worker: UniWorkerDefinition
    when: Optional[str] = None
    every_sec: Optional[int] = None
    alone: bool

    @field_validator('every_sec')
    @classmethod
    def validate_every_sec(cls, v: Optional[int], info: ValidationInfo) -> Optional[int]:
        if v is None:
            return v
        if not isinstance(v, int):
            TypeError('Invalid type. must be int')
        if v <= 1:
            raise ValueError('Must be > 1')
        if 60 % v:
            raise ValueError('60 must be a multiple of N')
        return v

    @model_validator(mode='after')
    def validate_all(self) -> 'UniCronTaskDefinition':
        when = self.when
        every_sec = self.every_sec
        if not ((when is not None) ^ (every_sec is not None)):
            raise ValueError(f'cron "{self.name}" has property conflict in (when, every_sec). one from it must be None')
        return self
