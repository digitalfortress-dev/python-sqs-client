import json
import threading
import uuid

from sqs_client.publisher import Publisher


class Task:
    """
    This class represents a task to send and receive messages to an SQS queue
    """

    def __init__(
        self,
        sqs_client,
        queue_name,
        callback,
        max_number_of_messages=1,
        visibility_timeout=30,
        wait_time_seconds=20,
        delay_seconds=0,
        lazy=False,
    ):
        """
        Initializes the Task class.

        Args:
            sqs_client: (SQSClient) The SQSClient of task.
            queue_name: (string) The name of the SQS queue you want to send and receive messages.
            callback: (function) The callback function you want to use to process the message.
            max_number_of_messages: (integer) The maximum number of messages to return.
                Valid values: 1 to 10. Default: 1.
            visibility_timeout: (integer) The duration (in seconds) that the received messages are hidden from
                subsequent retrieve requests after being retrieved by a ReceiveMessage request.
                Default: 30
            wait_time_seconds: (integer) The duration (in seconds) for which the call waits for a message
                to arrive in the queue before returning.
                Default: 20.
            delay_seconds: (integer) The length of time, in seconds, for which to delay a specific message
                when use trigger function.
                Valid values: 0 to 900. Default: 0
            lazy: (bool) Make this task lazy mode. Trigger SQS message by task_name.trigger(*args, **kwargs)
        """
        self._id = str(uuid.uuid4())
        self._sqs_client = sqs_client
        self._queue_name = queue_name
        self._callback = callback
        self._max_number_of_messages = max_number_of_messages
        self._visibility_timeout = visibility_timeout
        self._wait_time_seconds = wait_time_seconds
        self._delay_seconds = delay_seconds
        self._lazy = lazy
        self._thread = self._create_subscribe_thread()
        self._publisher = Publisher(
            sqs_client=self._sqs_client,
            queue_name=self._queue_name,
            delay_seconds=self._delay_seconds,
        )

    def __call__(self, *args, **kwargs):
        """
        Direct invocation for the Task
        """
        return self._callback(*args, **kwargs)

    def get_id(self):
        """
        This function retrieves the ID of task
        Returns:
            The ID of task.
        """
        return self._id

    def _get_message_processing(self):
        """
        This function retrieves the message processing for the task
        Returns:
            (function) The message processing for the task.
        """
        if self._lazy:

            def process_message(message):
                payload = json.loads(message["Body"])
                self._callback(*payload["args"], **payload["kwargs"])

            return process_message
        else:
            return self._callback

    def subscribe(self):
        """
        This function continuously receives messages from an SQS queue and processes them through task's callback.
        """
        return self._sqs_client.subscribe(
            queue_name=self._queue_name,
            callback=self._get_message_processing(),
            max_number_of_messages=self._max_number_of_messages,
            visibility_timeout=self._visibility_timeout,
            wait_time_seconds=self._wait_time_seconds,
        )

    def _create_subscribe_thread(self):
        """
        This function creates an asynchronous thread to continuously receive messages
            from the SQS queue and processes them through task's callback.
        Returns:
            (Thread) The asynchronous thread to continuously receive messages from the SQS queue
        """
        thread = threading.Thread(target=self.subscribe, name=self._id)
        thread.start()
        return thread

    def check_health(self):
        """
        This function performs a health check on the entire task list, analyzing the health of all its registered tasks
        Returns:
            (bool) The health of all its registered tasks.
        """
        return self._thread.is_alive()

    def trigger(self, *args, **kwargs):
        """
        This function allows you to publish a message to the SQS queue to trigger the callback function later.
        Only work on lazy mode
        """
        if not self._lazy:
            raise Exception("Trigger function only work on lazy mode")

        self._publisher.publish_lazy(*args, **kwargs)
