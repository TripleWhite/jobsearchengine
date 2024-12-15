import unittest
from app.services.ai_service import parse_job_description, parse_resume, match_jobs
from tests.base import BaseTestCase

class TestAIService(BaseTestCase):
    def test_parse_job_description_success(self):
        # Mock successful response
        mock_response = {
            "content": '''{
                "job_title": "资深Java后端工程师",
                "company_name": "ABC科技",
                "location": "北京",
                "responsibilities": ["设计和开发后端服务", "优化系统性能"],
                "requirements": ["3年以上Java开发经验", "熟悉Spring框架"]
            }'''
        }
        self.mcp_mock.use_tool.return_value = mock_response

        result = parse_job_description("测试职位描述")
        
        # Verify MCP tool was called correctly
        self.mcp_mock.use_tool.assert_called_once()
        call_args = self.mcp_mock.use_tool.call_args[1]
        self.assertEqual(call_args['server_name'], 'siliconflow')
        self.assertEqual(call_args['tool_name'], 'json_mode')
        
        # Verify parsed result
        self.assertEqual(result['job_title'], "资深Java后端工程师")
        self.assertEqual(result['company_name'], "ABC科技")
        self.assertEqual(result['location'], "北京")
        self.assertEqual(len(result['responsibilities']), 2)
        self.assertEqual(len(result['requirements']), 2)

    def test_parse_job_description_missing_fields(self):
        # Mock response with missing fields
        mock_response = {
            "content": '{"job_title": "测试职位"}'
        }
        self.mcp_mock.use_tool.return_value = mock_response

        with self.assertRaises(ValueError) as context:
            parse_job_description("测试职位描述")
        
        self.assertTrue('Missing required field' in str(context.exception))

    def test_parse_resume_success(self):
        # Mock successful response
        mock_response = {
            "content": '''{
                "technical_analysis": {
                    "tech_stack": ["Java", "Python"],
                    "depth_evaluation": "技术基础扎实",
                    "learning_ability": "学习能力强",
                    "practical_experience": "有实际项目经验"
                },
                "experience_analysis": {
                    "years": 3,
                    "career_path": "开发工程师",
                    "project_highlights": ["项目A", "项目B"],
                    "problem_solving": "问题解决能力强"
                },
                "education_analysis": {
                    "background": "计算机科学学士",
                    "knowledge_base": "基础知识扎实",
                    "continuous_learning": "持续学习新技术"
                },
                "core_competencies": {
                    "key_skills": ["编程", "系统设计"],
                    "unique_strengths": "快速学习能力",
                    "soft_skills": ["沟通", "团队协作"]
                },
                "career_analysis": {
                    "suitable_positions": ["后端工程师"],
                    "potential_fields": ["云计算"],
                    "development_suggestions": "建议深入云原生技术",
                    "challenges": ["需要加强架构设计能力"]
                }
            }'''
        }
        self.mcp_mock.use_tool.return_value = mock_response

        result = parse_resume("测试简历内容")
        
        # Verify MCP tool was called correctly
        self.mcp_mock.use_tool.assert_called_once()
        call_args = self.mcp_mock.use_tool.call_args[1]
        self.assertEqual(call_args['server_name'], 'siliconflow')
        self.assertEqual(call_args['tool_name'], 'json_mode')
        
        # Verify parsed result
        self.assertIn('technical_analysis', result)
        self.assertIn('experience_analysis', result)
        self.assertIn('education_analysis', result)
        self.assertIn('core_competencies', result)
        self.assertIn('career_analysis', result)

    def test_parse_resume_empty_input(self):
        with self.assertRaises(ValueError) as context:
            parse_resume("")
        
        self.assertTrue('Resume text cannot be empty' in str(context.exception))

    def test_match_jobs_success(self):
        # Mock successful response
        mock_response = {
            "content": '''[{
                "job_id": 1,
                "match_score": 85,
                "match_analysis": "技能匹配度高",
                "advantages": ["技术栈匹配", "经验充足"],
                "challenges": ["需要学习新技术"],
                "suggestions": ["提前了解项目架构"]
            }]'''
        }
        self.mcp_mock.use_tool.return_value = mock_response

        resume_data = {
            "technical_analysis": {"tech_stack": ["Python", "Java"]}
        }
        jobs = [{"id": 1, "title": "测试职位"}]

        result = match_jobs(resume_data, "软件工程师", "北京", jobs)
        
        # Verify MCP tool was called correctly
        self.mcp_mock.use_tool.assert_called_once()
        call_args = self.mcp_mock.use_tool.call_args[1]
        self.assertEqual(call_args['server_name'], 'siliconflow')
        self.assertEqual(call_args['tool_name'], 'json_mode')
        
        # Verify matched result
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['job_id'], 1)
        self.assertEqual(result[0]['match_score'], 85)
        self.assertIn('match_analysis', result[0])
        self.assertIn('advantages', result[0])
        self.assertIn('challenges', result[0])
        self.assertIn('suggestions', result[0])

    def test_match_jobs_empty_input(self):
        with self.assertRaises(ValueError) as context:
            match_jobs({}, "", "", [])
        
        self.assertTrue('Resume data and jobs list cannot be empty' in str(context.exception))

    def test_match_jobs_invalid_response(self):
        # Mock invalid response
        mock_response = {
            "content": '{"invalid": "format"}'
        }
        self.mcp_mock.use_tool.return_value = mock_response

        resume_data = {
            "technical_analysis": {"tech_stack": ["Python", "Java"]}
        }
        jobs = [{"id": 1, "title": "测试职位"}]

        result = match_jobs(resume_data, "软件工程师", "北京", jobs)
        
        # Should handle invalid format gracefully and return empty list
        self.assertEqual(result, [])
