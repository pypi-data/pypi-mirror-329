from ul_unipipeline.definitions.uni_definition import UniDefinition
from ul_unipipeline.definitions.uni_module_definition import UniModuleDefinition


class UniCodecDefinition(UniDefinition):
    name: str
    encoder_type: UniModuleDefinition
    decoder_type: UniModuleDefinition
