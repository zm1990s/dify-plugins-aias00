from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

class ElasticsearchProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        此插件不需要全局凭证，认证信息在每次调用时提供
        """
        # 此插件不需要全局凭证验证，所有认证信息都在工具调用时提供
        pass

