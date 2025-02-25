from ul_unipipeline.message.uni_message import UniMessage


class EnderAfterCronAnswerMessage(UniMessage):
    value: str
    result: int
