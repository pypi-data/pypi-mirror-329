from typing import Optional
from uuid import UUID

from ul_unipipeline.definitions.uni_definition import UniDefinition
from ul_unipipeline.definitions.uni_module_definition import UniModuleDefinition


class UniBrokerDefinition(UniDefinition):
    id: UUID
    type: UniModuleDefinition

    retry_max_count: int
    retry_delay_s: int

    external: Optional[str] = None

    content_type: str
    compression: Optional[str] = None

    @property
    def marked_as_external(self) -> bool:
        return self.external is not None
