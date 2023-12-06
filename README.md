<p align="center">
  <a href="https://www.digitalfortress.dev/">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://instalent-bucket-s3.s3.ap-southeast-1.amazonaws.com/logo/Digital+Fortress+-+Logo.png">
      <img alt="Digital Fortress logo" src="https://instalent-bucket-s3.s3.ap-southeast-1.amazonaws.com/logo/Digital+Fortress+-+Logo.png">
    </picture>    
  </a>
</p>

---

# Git Repository Template

## Getting Started

Install package
```commandline
pip install sqs-client
```

## Example


```python
from sqs_client.client import SQSClient

sqs_client = SQSClient()


# Subscribe to an SQS
@sqs_client.task(
    queue_name="sqs-queue-name",
    lazy=True,
    wait_time_seconds=0,
    visibility_timeout=300,
)
def test_task(message):
    print("test_task received:", message)


# Publish a message
test_task.trigger("Test message")
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
