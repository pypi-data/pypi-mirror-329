from typing import Any, Protocol


class SQSClient(Protocol):
    def delete_message(self, QueueUrl: str, ReceiptHandle: str) -> None: ...

    def send_message(self, QueueUrl: str, MessageBody: str) -> dict[str, Any]: ...

    def get_queue_url(self, QueueName: str) -> dict[str, Any]: ...

    def receive_message(
        self,
        QueueUrl: str,
        MaxNumberOfMessages: int,
        WaitTimeSeconds: int,
        MessageAttributeNames: list[str],
    ) -> dict[str, Any]: ...
