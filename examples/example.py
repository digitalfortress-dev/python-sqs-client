from sqs_client.client import SQSClient

sqs_client = SQSClient()


@sqs_client.task(
    queue_name="sqs-queue-name",
    lazy=True,
    wait_time_seconds=0,
    visibility_timeout=300,
)
def test_task(message):
    print("test_task received:", message)


test_task.trigger("Test message")
