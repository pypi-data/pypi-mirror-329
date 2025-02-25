from example.messages.ender_after_cron_answer_message import EnderAfterCronAnswerMessage
from example.messages.ender_after_cron_input_message import EnderAfterCronInputMessage
from ul_unipipeline.worker.uni_worker import UniWorker
from ul_unipipeline.worker.uni_worker_consumer_message import UniWorkerConsumerMessage


class EnderAfterCronWorker(UniWorker[EnderAfterCronInputMessage, EnderAfterCronAnswerMessage]):
    def handle_message(self, msg: UniWorkerConsumerMessage[EnderAfterCronInputMessage]) -> EnderAfterCronAnswerMessage:
        return EnderAfterCronAnswerMessage(
            value=f'after_cron => {msg.payload.value}',
            result=msg.payload.count * 3,
        )
