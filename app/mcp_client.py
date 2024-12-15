"""
MCP client implementation for development and testing purposes.
The actual MCP client in production is provided by Cline at runtime.
"""

import requests
from flask import current_app

class DevMCPClient:
    """
    Development MCP client that directly communicates with SiliconFlow API.
    This is used when the Cline-provided MCP client is not available.
    """
    def __init__(self):
        self.base_url = "https://api.siliconflow.cn/v1"
        self.headers = {
            "Authorization": "Bearer sk-mftgyyhnsaejnfijrcicniglezqrnizyrbrogpoqfdqkneaz",
            "Content-Type": "application/json"
        }

    def use_tool(self, server_name, tool_name, arguments):
        """
        使用 SiliconFlow API 工具。
        目前仅支持 json_mode 工具。
        """
        if server_name != "siliconflow" or tool_name != "json_mode":
            raise ValueError(f"Unsupported tool: {server_name}/{tool_name}")
        
        # 确保使用 Qwen 模型
        arguments["model"] = "Qwen/Qwen2.5-72B-Instruct-128K"
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=arguments
            )
            
            if response.status_code != 200:
                raise Exception(f"API error: {response.text}")
                
            result = response.json()
            return {
                "content": result["choices"][0]["message"]["content"]
            }
        except Exception as e:
            current_app.logger.error(f"SiliconFlow API error: {str(e)}")
            raise

def get_mcp_client():
    """
    获取 MCP 客户端。
    如果 Cline 提供的 MCP 客户端可用，则使用它；
    否则使用开发版 MCP 客户端。
    """
    try:
        # 尝试获取 Cline 提供的 MCP 客户端
        return current_app.mcp
    except AttributeError:
        # 如果 Cline MCP 客户端不可用，使用开发版客户端
        if not hasattr(current_app, '_dev_mcp'):
            current_app._dev_mcp = DevMCPClient()
        return current_app._dev_mcp
