from ul_unipipeline.definitions.uni_definition import UniDefinition
from ul_unipipeline.definitions.uni_module_definition import UniModuleDefinition


class UniMessageDefinition(UniDefinition):
    name: str
    type: UniModuleDefinition
