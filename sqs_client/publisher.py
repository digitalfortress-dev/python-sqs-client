import json


class Publisher:
    """
    This class represents a publisher to send  messages to an SQS queue
    """

    def __init__(
        self,
        sqs_client,
        queue_name,
        delay_seconds=0,
    ):
        """
        Initializes the Publisher class.

        Args:
            sqs_client: (SQSClient) The SQSClient of task.
            queue_name: (string) The name of the SQS queue you want to send and receive messages.
            delay_seconds: (integer) The length of time, in seconds, for which to delay a specific message.
                Valid values: 0 to 900. Default: 0
        """
        self._sqs_client = sqs_client
        self._queue_name = queue_name
        self._delay_seconds = delay_seconds

    def publish(self, message):
        """
        This function allows you to publish a message to an SQS queue.

        Args:
            message: (string) The message content to be sent.
        """
        self._sqs_client.publish(
            queue_name=self._queue_name,
            delay_seconds=self._delay_seconds,
            message=message,
        )

    def publish_lazy(self, *args, **kwargs):
        """
        This function allows you to publish a message in lazy mode.
        """
        self._sqs_client.publish(
            queue_name=self._queue_name,
            delay_seconds=self._delay_seconds,
            message=json.dumps(
                {
                    "args": args,
                    "kwargs": kwargs,
                }
            ),
        )
