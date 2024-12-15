import json
from typing import Dict, Any, List
from flask import current_app
from app.mcp_client import get_mcp_client

def parse_job_description(raw_jd_text: str) -> Dict[str, Any]:
    """
    使用 SiliconFlow API 解析职位描述文本，提取结构化信息
    """
    messages = [
        {
            "role": "system",
            "content": """你是一个专业的职位信息提取助手。请从职位描述文本中提取以下关键信息并以JSON格式返回:
{
    "job_title": "职位名称",
    "company_name": "公司名称",
    "location": "工作地点",
    "responsibilities": ["工作职责1", "工作职责2", ...],
    "requirements": ["职位要求1", "职位要求2", ...]
}

请确保每个字段都有值。如果某些信息在文本中未明确提供，请根据上下文合理推断。"""
        },
        {
            "role": "user",
            "content": raw_jd_text
        }
    ]

    try:
        mcp = get_mcp_client()
        response = mcp.use_tool(
            server_name="siliconflow",
            tool_name="json_mode",
            arguments={
                "messages": messages,
                "response_format": {"type": "json_object"},
                "temperature": 0.7
            }
        )
        
        # 解析响应
        parsed_data = json.loads(response.get("content", "{}"))
        
        # 确保所有必需字段都存在
        required_fields = ['job_title', 'company_name', 'location', 'responsibilities', 'requirements']
        for field in required_fields:
            if field not in parsed_data:
                raise ValueError(f"Missing required field: {field}")
        
        return parsed_data

    except Exception as e:
        current_app.logger.error(f"Error parsing job description: {str(e)}")
        raise ValueError(f"Failed to parse job description: {str(e)}")

def parse_resume(resume_text: str) -> Dict[str, Any]:
    """
    使用 SiliconFlow API 深入解析简历文本，分析用户能力和潜力
    """
    if not resume_text:
        raise ValueError("Resume text cannot be empty")

    messages = [
        {
            "role": "system",
            "content": """你是一位资深的人才评估专家。请对简历进行深入分析，并以以下JSON格式返回分析结果:
{
    "technical_analysis": {
        "tech_stack": ["技术1", "技术2", ...],
        "depth_evaluation": "技术深度评估",
        "learning_ability": "学习能力评估",
        "practical_experience": "技术实践经验总结"
    },
    "experience_analysis": {
        "years": 工作年限数字,
        "career_path": "职业发展轨迹",
        "project_highlights": ["项目亮点1", "项目亮点2", ...],
        "problem_solving": "解决问题能力评估"
    },
    "education_analysis": {
        "background": "最高学历和专业",
        "knowledge_base": "专业知识储备评估",
        "continuous_learning": "持续学习能力评估"
    },
    "core_competencies": {
        "key_skills": ["核心技能1", "核心技能2", ...],
        "unique_strengths": "独特优势",
        "soft_skills": ["软技能1", "软技能2", ...]
    },
    "career_analysis": {
        "suitable_positions": ["适合职位1", "适合职位2", ...],
        "potential_fields": ["潜力领域1", "潜力领域2", ...],
        "development_suggestions": "发展建议",
        "challenges": "可能面临的挑战"
    }
}"""
        },
        {
            "role": "user",
            "content": resume_text
        }
    ]

    try:
        mcp = get_mcp_client()
        response = mcp.use_tool(
            server_name="siliconflow",
            tool_name="json_mode",
            arguments={
                "messages": messages,
                "response_format": {"type": "json_object"},
                "temperature": 0.7
            }
        )
        
        # 解析响应
        parsed_data = json.loads(response.get("content", "{}"))
        
        # 验证关键字段
        required_sections = [
            'technical_analysis', 
            'experience_analysis', 
            'education_analysis', 
            'core_competencies', 
            'career_analysis'
        ]
        
        # 如果缺少任何部分，提供默认值
        for section in required_sections:
            if section not in parsed_data:
                parsed_data[section] = {"note": "无法从简历中提取相关信息"}
        
        return parsed_data

    except Exception as e:
        current_app.logger.error(f"Error parsing resume: {str(e)}")
        raise ValueError(f"Failed to parse resume: {str(e)}")

def match_jobs(resume_data: Dict[str, Any], desired_position: str, desired_location: str, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    使用 SiliconFlow API 进行深度职位匹配分析
    """
    if not resume_data or not jobs:
        raise ValueError("Resume data and jobs list cannot be empty")

    messages = [
        {
            "role": "system",
            "content": """你是一位专业的职业发展顾问。请基于候选人的简历分析和职位要求进行智能匹配分析，并以JSON数组格式返回结果。每个匹配项应包含:
{
    "job_id": 职位ID,
    "match_score": 匹配度评分(0-100),
    "match_analysis": "详细的匹配分析",
    "advantages": ["优势1", "优势2", ...],
    "challenges": ["挑战1", "挑战2", ...],
    "suggestions": ["建议1", "建议2", ...]
}

请考虑以下维度进行分析:
1. 能力匹配度: 技术栈匹配程度、项目经验相关性、专业知识覆盖度、工作年限适配性
2. 发展潜力: 职位是否符合职业发展轨迹、快速适应和成长潜力、核心竞争力发挥
3. 职业规划: 是否符合发展方向、成长空间、工作地点匹配度
4. 综合评估: 优势和不足、需要提升的方面、入职后的发展建议"""
        },
        {
            "role": "user",
            "content": json.dumps({
                "resume_data": resume_data,
                "desired_position": desired_position,
                "desired_location": desired_location,
                "jobs": jobs
            }, ensure_ascii=False)
        }
    ]

    try:
        mcp = get_mcp_client()
        response = mcp.use_tool(
            server_name="siliconflow",
            tool_name="json_mode",
            arguments={
                "messages": messages,
                "response_format": {"type": "json_object"},
                "temperature": 0.7
            }
        )
        
        # 解析响应
        result = json.loads(response.get("content", "[]"))
        
        # 如果返回的是对象且包含recommendations字段，使用该字段
        if isinstance(result, dict) and 'recommendations' in result:
            result = result['recommendations']
        # 如果返回的不是列表，返回空列表
        elif not isinstance(result, list):
            return []
        
        # 验证和规范化每个推荐项
        validated_recommendations = []
        for item in result:
            if isinstance(item, dict) and 'job_id' in item:
                recommendation = {
                    'job_id': item['job_id'],
                    'match_score': item.get('match_score', 0),
                    'match_analysis': item.get('match_analysis', '未提供匹配分析'),
                    'advantages': item.get('advantages', []),
                    'challenges': item.get('challenges', []),
                    'suggestions': item.get('suggestions', [])
                }
                validated_recommendations.append(recommendation)
        
        # 按匹配度排序
        validated_recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        return validated_recommendations

    except Exception as e:
        current_app.logger.error(f"Error matching jobs: {str(e)}")
        raise ValueError(f"Failed to match jobs: {str(e)}")
