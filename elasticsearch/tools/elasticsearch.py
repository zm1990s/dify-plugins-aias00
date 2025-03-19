from collections.abc import Generator
from typing import Any

from elasticsearch import Elasticsearch
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class ElasticsearchTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        index_name = tool_parameters.get("index_name")
        es_host = tool_parameters.get('es_host')
        es_username = tool_parameters.get('es_username')
        es_password = tool_parameters.get('es_password')

        if 'content' not in tool_parameters:
            yield self.create_json_message({"message": 'Send Failed, content is missing'})
            return
        content = tool_parameters.get("content")

        if es_username and es_password:
            es = Elasticsearch(
                [es_host],
                http_auth=(es_username, es_password),
                verify_certs=False
            )
        else:
            es = Elasticsearch([es_host], verify_certs=False)
        try:
            response = es.index(index=index_name, body=content, timeout="30s")
        except Exception as e:
            yield self.create_json_message({"message": f"Write Failed: {str(e)}"})
            return
        return {
            "status": "success",
            "document_id": response["_id"],
            "index": response["_index"]
        }
