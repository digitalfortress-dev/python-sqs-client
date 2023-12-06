from logging import exception

import boto3

from sqs_client.task import Task


class SQSClient:
    """
    This class represents a client for interacting with the SQS service.

    It provides methods for sending and receiving messages.
    """

    def __init__(
        self,
        region_name=None,
        aws_access_key_id=None,
        aws_secret_access_key=None,
    ):
        """
        Initializes the SQSClient class.

        Args:
            region_name: (string) The name of the region associated with the client.
            aws_access_key_id: (string) The access key to use when creating
                the client.  This is entirely optional, and if not provided,
                the credentials configured for the session will automatically
                be used.  You only need to provide this argument if you want
                to override the credentials used for this specific client.
            aws_access_key_id: (string) The access key to use when creating
                the client.  This is entirely optional, and if not provided,
                the credentials configured for the session will automatically
                be used.  You only need to provide this argument if you want
                to override the credentials used for this specific client.
        """
        self._boto3_client = boto3.client(
            "sqs",
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self._list_queue_urls = None
        self._task_list = {}

    def get_task_list(self):
        """
        This function retrieves the list of tasks currently
        Returns:
            The list of tasks.
        """
        return self._task_list

    def check_health(self):
        """
        This function performs a health check on the entire task list, analyzing the health of all its registered tasks
        Returns:
            (bool) The health of all its registered tasks.
        """
        return all([task.check_health() for task in self._task_list.values()])

    def task(
        self,
        queue_name,
        max_number_of_messages=1,
        visibility_timeout=30,
        wait_time_seconds=20,
        lazy=False,
    ):
        """
        Decorator to create a task object out of any callable.

        Args:
            queue_name: (string) The name of the SQS queue you want to create a task.
            max_number_of_messages: (integer) The maximum number of messages to return.
                Valid values: 1 to 10. Default: 1.
            visibility_timeout: (integer) The duration (in seconds) that the received messages are hidden from
                subsequent retrieve requests after being retrieved by a ReceiveMessage request.
                Default: 30
            wait_time_seconds: (integer) The duration (in seconds) for which the call waits for a message
                to arrive in the queue before returning.
                Default: 20.
            lazy: (bool) Make this task lazy mode. Trigger SQS message by task_name.trigger(*args, **kwargs)

        Examples:
            @sqs_client.task(queue="dev-retailer_getting_order_sqs")
            def test_task(message):
                print(message)

        Returns:
            The task object.
        """

        def inner_create_task(callback):
            task = Task(
                sqs_client=self,
                queue_name=queue_name,
                callback=callback,
                max_number_of_messages=max_number_of_messages,
                visibility_timeout=visibility_timeout,
                wait_time_seconds=wait_time_seconds,
                lazy=lazy,
            )
            self._task_list[task.get_id()] = task
            return task

        return inner_create_task

    def get_queue_url_by_name(self, queue_name):
        """
        This function retrieves the URL of an SQS queue based on its name.

        Args:
            queue_name: (string) The name of the SQS queue you want to find.
        """
        if not self._list_queue_urls:
            response = self._boto3_client.list_queues()

            self._list_queue_urls = response["QueueUrls"]

        for queue_url in self._list_queue_urls:
            if queue_url.endswith(f"/{queue_name}"):
                return queue_url

        return None

    def delete_message(self, queue_name, message):
        """
        This function permanently removes a message from an SQS queue.

        Args:
            queue_name: (string) The name of the SQS queue you want to delete message.
            message: The SQS message you want to remove.
        """
        receipt_handle = message["ReceiptHandle"]
        self._boto3_client.delete_message(
            QueueUrl=self.get_queue_url_by_name(queue_name),
            ReceiptHandle=receipt_handle,
        )

    def subscribe(
        self,
        queue_name,
        callback,
        max_number_of_messages=1,
        visibility_timeout=30,
        wait_time_seconds=20,
    ):
        """
        This function continuously receives messages from an SQS queue and processes them through a callback.

        Args:
            queue_name: (string) The name of the SQS queue you want to receives messages.
            callback: (function) The callback function you want to use to process the message.
            max_number_of_messages: (integer) The maximum number of messages to return.
                Valid values: 1 to 10. Default: 1.
            visibility_timeout: (integer) The duration (in seconds) that the received messages are hidden from
                subsequent retrieve requests after being retrieved by a ReceiveMessage request.
                Default: 30
            wait_time_seconds: (integer) The duration (in seconds) for which the call waits for a message
                to arrive in the queue before returning.
                Default: 20.
        """
        while True:
            messages = self._boto3_client.receive_message(
                QueueUrl=self.get_queue_url_by_name(queue_name),
                MaxNumberOfMessages=max_number_of_messages,
                VisibilityTimeout=visibility_timeout,
                WaitTimeSeconds=wait_time_seconds,
            )

            if "Messages" in messages and messages["Messages"]:
                for message in messages["Messages"]:
                    try:
                        callback(message)
                    except Exception as e:
                        exception(e)

                    self.delete_message(queue_name, message)

    def publish(
        self,
        queue_name,
        message,
        delay_seconds=0,
    ):
        """
        This function allows you to publish a message to an SQS queue.

        Args:
            queue_name: (string) The name of the SQS queue you want to receive messages.
            message: (string) The message content to be sent.
            delay_seconds: (integer) The length of time, in seconds, for which to delay a specific message.
                Valid values: 0 to 900. Default: 0
        """
        self._boto3_client.send_message(
            QueueUrl=self.get_queue_url_by_name(queue_name),
            DelaySeconds=delay_seconds,
            MessageBody=message,
        )
