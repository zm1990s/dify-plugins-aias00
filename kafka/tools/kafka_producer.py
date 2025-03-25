from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from kafka import KafkaProducer

class KafkaTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # Get required parameters
        bootstrap_servers = tool_parameters.get("bootstrap_servers")
        topic = tool_parameters.get("topic") 
        message = tool_parameters.get("message")

        # Validate parameters
        if not all([bootstrap_servers, topic, message]):
            yield self.create_json_message({
                "error": "Missing required parameters. Please provide bootstrap_servers, topic and message."
            })
            return

        try:
            # Initialize producer with json serializer
            producer = KafkaProducer(
                bootstrap_servers=[bootstrap_servers],
                value_serializer=lambda x: x.encode('utf-8') if isinstance(x, str) else str(x).encode('utf-8')
            )

            # Send message
            future = producer.send(topic, value=message)
            
            # Wait for message to be delivered
            record_metadata = future.get(timeout=10)
            
            producer.flush()
            producer.close()

            # Return success message with metadata
            yield self.create_json_message({
                "status": "success",
                "message": f"Message successfully written to {topic}",
                "metadata": {
                    "topic": record_metadata.topic,
                    "partition": record_metadata.partition,
                    "offset": record_metadata.offset
                }
            })

        except Exception as e:
            yield self.create_json_message({
                "status": "error",
                "message": f"Failed to write message: {str(e)}"
            })
            return

