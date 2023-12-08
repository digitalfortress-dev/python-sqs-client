<p align="center">
  <a href="https://www.digitalfortress.dev/">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://instalent-bucket-s3.s3.ap-southeast-1.amazonaws.com/logo/Digital+Fortress+-+Logo.png">
      <img alt="Digital Fortress logo" src="https://instalent-bucket-s3.s3.ap-southeast-1.amazonaws.com/logo/Digital+Fortress+-+Logo.png">
    </picture>    
  </a>
</p>

---

# Python SQS client

## Getting Started

Install package
```commandline
pip install sqs-client
```

## Example

#### Subscribe

```python
from sqs_client.client import SQSClient

sqs_client = SQSClient()


# Subscribe to a SQS
@sqs_client.task(
    queue_name="sqs-queue-name",
    wait_time_seconds=0,
    visibility_timeout=300,
    daemon=False,
)
def test_task(message):
    print("test_task received:", message)
```

#### Publish
```python
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
```

### Lazy mode

Faster to subscribe and publish a message to SQS

```python
from sqs_client.client import SQSClient

sqs_client = SQSClient()


# Subscribe to a SQS
@sqs_client.task(
    queue_name="sqs-queue-name",
    lazy=True,
    daemon=False,
    wait_time_seconds=0,
    visibility_timeout=300,
)
def test_task(message, abc):
    print("test_task received message:", message)
    print("test_task received abc:", abc)


# Publish a message
test_task.trigger("Test message", abc=1)
```

Publish a lazy mode message without subscribe

```python
from sqs_client.client import SQSClient
from sqs_client.publisher import Publisher

sqs_client = SQSClient()

publisher = Publisher(
    sqs_client=sqs_client,
    queue_name="sqs-queue-name",
)

publisher.publish_lazy("Test lazy message", abc=1)
```

## License

This project is Copyright (c) 2023 and onwards Digital Fortress. It is free software and may be redistributed under the terms specified in the [LICENSE] file.

[LICENSE]: /LICENSE

## About
<a href="https://www.digitalfortress.dev/">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://instalent-bucket-s3.s3.ap-southeast-1.amazonaws.com/logo/Digital+Fortress+-+Logo.png">
    <img alt="Digital Fortress logo" src="https://instalent-bucket-s3.s3.ap-southeast-1.amazonaws.com/logo/Digital+Fortress+-+Logo.png" width="160">
  </picture>
</a>

This project is made and maintained by Digital Fortress.

We are an experienced team in R&D, software, hardware, cross-platform mobile and DevOps.

See more of [our projects][projects] or do you need to complete one?

-> [Let’s connect with us][website]

[projects]: https://github.com/digitalfortress-dev
[website]: https://www.digitalfortress.dev
