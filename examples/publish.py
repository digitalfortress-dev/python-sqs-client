from sqs_client.client import SQSClient
from sqs_client.publisher import Publisher

sqs_client = SQSClient()

sqs_client.publish(
    queue_name="sqs-queue-name",
    message="test message",
)

# or

publisher = Publisher(
    sqs_client=sqs_client,
    queue_name="sqs-queue-name",
)

publisher.publish("test message")

# publish lazy mode message
publisher.publish_lazy("test lazy message", abc=1)
