from sqs_client.client import SQSClient

sqs_client = SQSClient()


# Subscribe to a SQS
@sqs_client.task(
    queue_name="sqs-queue-name",
    wait_time_seconds=20,
    visibility_timeout=300,
    daemon=False,
)
def test_task(message):
    print("test_task received:", message)
