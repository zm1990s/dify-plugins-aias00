from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class KafkaTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # Get parameters
        bootstrap_servers = tool_parameters.get("bootstrap_servers")
        topic = tool_parameters.get("topic")
        group_id = tool_parameters.get("group_id")
        delimiter = tool_parameters.get("delimiter", "\n")
        if not all([bootstrap_servers, topic, group_id]):
            yield self.create_json_message({
                "error": "Missing required parameters. Please provide bootstrap_servers, topic and group_id."
            })
            return

        try:
            from kafka import KafkaConsumer

            # Create consumer without JSON deserialization
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=bootstrap_servers,
                group_id=group_id,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda x: x.decode('utf-8')  # Only decode as string, don't parse JSON
            )

            # Consume messages with timeout
            messages = []
            try:
                # Poll for messages with a timeout of 10 seconds
                message_pack = consumer.poll(timeout_ms=10000, max_records=10)
                
                # Process received messages
                for topic_partition, partition_messages in message_pack.items():
                    for message in partition_messages:
                        messages.append(message.value)
                
            finally:
                # Always close the consumer
                consumer.close()

            if messages:
                # Join messages into a single string with newlines
                messages_text = delimiter.join(messages)
                yield self.create_text_message(messages_text)
            else:
                yield self.create_json_message({
                    "message": "No messages found in topic"
                })

        except Exception as e:
            yield self.create_json_message({
                "error": f"Failed to consume messages: {str(e)}"
            })
