from example.messages.input_message import InputMessage
from ul_unipipeline.worker.uni_worker import UniWorker
from ul_unipipeline.worker.uni_worker_consumer_message import UniWorkerConsumerMessage


class AutoRetryWorker(UniWorker[InputMessage, None]):
    def handle_message(self, msg: UniWorkerConsumerMessage[InputMessage]) -> None:
        raise RuntimeError('some critical runtime error. like db deadlock')
