from typing import Set, Optional
from uuid import UUID

from ul_unipipeline.definitions.uni_broker_definition import UniBrokerDefinition
from ul_unipipeline.definitions.uni_definition import UniDefinition
from ul_unipipeline.definitions.uni_message_definition import UniMessageDefinition
from ul_unipipeline.definitions.uni_module_definition import UniModuleDefinition
from ul_unipipeline.definitions.uni_waiting_definition import UniWaitingDefinition


class UniWorkerDefinition(UniDefinition):
    id: UUID
    name: str
    broker: UniBrokerDefinition
    type: Optional[UniModuleDefinition] = None
    topic: str
    prefetch_count: int
    error_topic: str
    error_payload_topic: str
    answer_topic: str
    input_message: UniMessageDefinition
    answer_message: Optional[UniMessageDefinition] = None
    output_workers: Set[str]
    waitings: Set[UniWaitingDefinition]
    external: Optional[str] = None
    input_unwrapped: bool
    answer_unwrapped: bool

    @property
    def marked_as_external(self) -> bool:
        return self.external is not None

    @property
    def need_answer(self) -> bool:
        return self.answer_message is not None
