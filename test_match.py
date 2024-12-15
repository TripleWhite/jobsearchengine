from flask import Flask
from app.services.ai_service import match_jobs
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

# 简历数据
resume_data = {
    "technical_analysis": {
        "tech_stack": ["Java", "Python", "Go", "Spring Boot", "Django", "Gin", "MySQL", "MongoDB", "Redis", "RabbitMQ", "Kafka", "Docker", "Kubernetes", "Jenkins"],
        "depth_evaluation": "深厚的技术背景，尤其在后端开发和服务端架构方面经验丰富",
        "learning_ability": "较强的学习能力，持续获取新技术认证",
        "practical_experience": "负责核心系统开发，成功带领团队完成架构转型"
    },
    "experience_analysis": {
        "years": 4,
        "career_path": "后端工程师到高级后端工程师",
        "project_highlights": ["核心支付系统开发", "微服务架构转型", "订单系统重构"],
        "problem_solving": "出色的问题解决能力，成功优化系统性能"
    }
}

# 职位列表
jobs = [
    {
        "id": 1,
        "title": "高级后端工程师",
        "company": "DEF科技",
        "location": "北京",
        "description": """
        职责：
        - 负责公司核心系统的设计和开发
        - 参与系统架构设计和技术选型
        - 解决系统性能瓶颈
        
        要求：
        - 5年以上后端开发经验
        - 精通 Java、Spring Boot
        - 熟悉分布式系统设计
        - 有大型项目经验
        """
    },
    {
        "id": 2,
        "title": "技术经理",
        "company": "GHI科技",
        "location": "上海",
        "description": """
        职责：
        - 带领团队完成项目开发
        - 负责技术架构规划
        - 把控项目质量和进度
        
        要求：
        - 8年以上开发经验
        - 3年以上团队管理经验
        - 精通后端技术栈
        - 优秀的沟通协调能力
        """
    }
]

with app.app_context():
    try:
        result = match_jobs(resume_data, "高级后端工程师", "北京", jobs)
        
        print("\n=== 职位匹配结果 ===")
        for match in result:
            print(f"\n职位 ID: {match['job_id']}")
            print(f"匹配度: {match['match_score']}%")
            print(f"匹配分析: {match['match_analysis']}")
            print("\n优势:")
            for adv in match['advantages']:
                print(f"- {adv}")
            print("\n挑战:")
            for chl in match['challenges']:
                print(f"- {chl}")
            print("\n建议:")
            for sug in match['suggestions']:
                print(f"- {sug}")
            print("\n" + "="*50)
            
    except Exception as e:
        print("错误:", str(e))
