from sqs_client.client import SQSClient

sqs_client = SQSClient()


# Subscribe to a SQS
@sqs_client.task(
    queue_name="sqs-queue-name",
    lazy=True,
    wait_time_seconds=0,
    visibility_timeout=300,
    daemon=False,
)
def test_task(message, abc):
    print("test_task received message:", message)
    print("test_task received abc:", abc)


# Publish a message
test_task.trigger("Test message", abc=1)
