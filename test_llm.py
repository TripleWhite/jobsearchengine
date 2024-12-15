from flask import Flask
from app.services.ai_service import parse_job_description
import json

class MCPClient:
    def __init__(self):
        self.base_url = "https://api.siliconflow.cn/v1"
        self.headers = {
            "Authorization": "Bearer sk-mftgyyhnsaejnfijrcicniglezqrnizyrbrogpoqfdqkneaz",
            "Content-Type": "application/json"
        }

    def use_tool(self, server_name, tool_name, arguments):
        if server_name != "siliconflow" or tool_name != "json_mode":
            raise ValueError(f"Unsupported tool: {server_name}/{tool_name}")
        
        # 确保使用 Qwen 模型
        arguments["model"] = "Qwen/Qwen2.5-72B-Instruct-128K"
        
        import requests
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

app = Flask(__name__)
app.config['TESTING'] = True
app.mcp = MCPClient()

test_jd = """
职位名称：高级后端工程师
公司：ABC科技有限公司
工作地点：北京市海淀区

工作职责：
1. 负责公司核心业务系统的设计和开发
2. 优化系统架构，提升系统性能和可扩展性
3. 参与技术方案评审，解决技术难题

任职要求：
1. 本科及以上学历，计算机相关专业
2. 5年以上后端开发经验
3. 精通 Java、Spring Boot、MySQL
4. 有大规模分布式系统开发经验
"""

with app.app_context():
    try:
        result = parse_job_description(test_jd)
        print("\n解析结果:")
        print("职位名称:", result.get('job_title'))
        print("公司:", result.get('company_name'))
        print("地点:", result.get('location'))
        print("\n工作职责:")
        for resp in result.get('responsibilities', []):
            print(f"- {resp}")
        print("\n任职要求:")
        for req in result.get('requirements', []):
            print(f"- {req}")
    except Exception as e:
        print("错误:", str(e))
