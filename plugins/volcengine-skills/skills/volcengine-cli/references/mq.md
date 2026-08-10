# Message Queue Service Notes

## Kafka and RocketMQ Need Pagination

Kafka and RocketMQ `DescribeInstances` require `PageNumber` and `PageSize`; omitting them returns an invalid page parameter error.

```bash
ve kafka DescribeInstances --body '{"RegionId":"cn-beijing","PageNumber":1,"PageSize":10}'
ve rocketmq DescribeInstances --body '{"RegionId":"cn-beijing","PageNumber":1,"PageSize":10}'
```

RabbitMQ `DescribeInstances` worked without the same pagination body in this environment.

## Safer Smoke-Test Surface

Kafka/RabbitMQ/RocketMQ allow-list read APIs returned successfully. Allow-list create/delete is a safer lifecycle candidate than full broker instance creation, but still requires explicit approval and final cleanup verification.

Observed in `cn-beijing`: Kafka, RabbitMQ, RocketMQ, and BMQ instance lists were empty. BMQ reported `cn-beijing-b` as sold out while other Beijing zones were available.
