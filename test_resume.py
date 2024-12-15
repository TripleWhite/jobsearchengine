from flask import Flask
from app.services.ai_service import parse_resume
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

test_resume = """
个人信息：
姓名：张三
年龄：28岁
教育背景：清华大学计算机科学与技术专业，硕士学位

工作经历：
2020-至今 ABC科技有限公司
职位：高级后端工程师
- 负责公司核心支付系统的设计和开发
- 优化系统性能，将交易响应时间降低50%
- 带领5人团队完成微服务架构转型

2018-2020 XYZ科技有限公司
职位：后端工程师
- 参与电商平台后端开发
- 实现订单系统重构，提升系统可扩展性
- 开发自动化测试框架，提高测试效率

技术技能：
- 编程语言：Java、Python、Go
- 框架：Spring Boot、Django、Gin
- 数据库：MySQL、MongoDB、Redis
- 中间件：RabbitMQ、Kafka
- 工具：Docker、Kubernetes、Jenkins

项目经验：
1. 分布式支付系统
- 使用 Spring Cloud 微服务架构
- 实现高并发交易处理，TPS达到5000
- 引入分布式事务解决方案

2. 实时数据分析平台
- 使用 Kafka + Flink 进行实时数据处理
- 实现实时数据大屏展示
- 开发数据异常监控系统

证书：
- AWS Certified Solutions Architect
- 阿里云高级工程师认证
"""

with app.app_context():
    try:
        result = parse_resume(test_resume)
        print("\n=== 简历分析结果 ===")
        
        print("\n技术分析:")
        tech = result['technical_analysis']
        print("技术栈:", ", ".join(tech['tech_stack']))
        print("技术深度:", tech['depth_evaluation'])
        print("学习能力:", tech['learning_ability'])
        print("实践经验:", tech['practical_experience'])
        
        print("\n经验分析:")
        exp = result['experience_analysis']
        print(f"工作年限: {exp['years']}年")
        print("职业发展:", exp['career_path'])
        print("项目亮点:", "\n- " + "\n- ".join(exp['project_highlights']))
        print("问题解决能力:", exp['problem_solving'])
        
        print("\n教育背景:")
        edu = result['education_analysis']
        print("学历:", edu['background'])
        print("知识储备:", edu['knowledge_base'])
        print("持续学习:", edu['continuous_learning'])
        
        print("\n核心竞争力:")
        comp = result['core_competencies']
        print("核心技能:", ", ".join(comp['key_skills']))
        print("独特优势:", comp['unique_strengths'])
        print("软实力:", ", ".join(comp['soft_skills']))
        
        print("\n职业分析:")
        career = result['career_analysis']
        print("适合职位:", ", ".join(career['suitable_positions']))
        print("潜力领域:", ", ".join(career['potential_fields']))
        print("发展建议:", career['development_suggestions'])
        print("潜在挑战:", career['challenges'])
        
    except Exception as e:
        print("错误:", str(e))
