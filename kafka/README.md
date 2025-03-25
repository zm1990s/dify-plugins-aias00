## kafka

**Author:** aias00
**Version:** 0.0.1
**Type:** tool

### Description

This plugin provides Kafka producer and consumer tools:

#### Kafka Consumer
- Consumes messages from specified Kafka topics
- Configurable bootstrap servers, topic name, and consumer group ID
- Supports message delimiter customization
- Auto decodes messages as UTF-8 strings
- Polls messages with timeout and auto-commit

#### Kafka Producer
- Produces messages to specified Kafka topics
- Configurable bootstrap servers and topic name
- Supports sending messages to Kafka topics
- Encodes messages as UTF-8 strings
