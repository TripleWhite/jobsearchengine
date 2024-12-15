import React, { useEffect, useState } from 'react';
import { Card, Input, Button, Typography, message, Spin, List, Collapse } from 'antd';
import { getProfile, updateResume, UserProfile as IUserProfile } from '../api/user';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Panel } = Collapse;

const UserProfile: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [profile, setProfile] = useState<IUserProfile | null>(null);
  const [resumeText, setResumeText] = useState('');

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const response = await getProfile();
      setProfile(response.user);
      if (response.user.resume_text) {
        setResumeText(response.user.resume_text);
      }
    } catch (error) {
      message.error('加载用户资料失败');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateResume = async () => {
    if (!resumeText.trim()) {
      message.error('请输入简历内容');
      return;
    }

    setUpdating(true);
    try {
      const response = await updateResume(resumeText);
      if (response.status === 'ok') {
        message.success('简历更新成功');
        // 重新加载用户资料以获取解析结果
        await loadProfile();
      } else {
        message.error(response.message || '更新失败');
      }
    } catch (error) {
      message.error('更新简历失败');
    } finally {
      setUpdating(false);
    }
  };

  const renderAnalysisSection = (title: string, data: any) => {
    if (!data) return null;

    const renderContent = (content: any) => {
      if (Array.isArray(content)) {
        return (
          <ul>
            {content.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        );
      } else if (typeof content === 'object') {
        return (
          <List
            itemLayout="vertical"
            dataSource={Object.entries(content)}
            renderItem={([key, value]) => (
              <List.Item>
                <Text strong>{key.replace(/_/g, ' ').toUpperCase()}: </Text>
                {renderContent(value)}
              </List.Item>
            )}
          />
        );
      }
      return <Text>{content}</Text>;
    };

    return (
      <Panel header={title} key={title}>
        {renderContent(data)}
      </Panel>
    );
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '40px' }}>
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>个人资料</Title>

      <Card style={{ marginBottom: '24px' }}>
        <div style={{ marginBottom: '16px' }}>
          <Text strong>邮箱：</Text>
          <Text>{profile?.email}</Text>
        </div>
        
        <div style={{ marginBottom: '16px' }}>
          <Text strong>姓名：</Text>
          <Text>{profile?.name || '未设置'}</Text>
        </div>
      </Card>

      <Card title="简历管理" style={{ marginBottom: '24px' }}>
        <div style={{ marginBottom: '16px' }}>
          <Paragraph>
            请在下方输入您的简历内容，系统会自动进行深度分析，帮助您找到最合适的职位。
          </Paragraph>
          <TextArea
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            placeholder="请输入您的简历内容..."
            rows={10}
            style={{ marginBottom: '16px' }}
          />
          <Button 
            type="primary" 
            onClick={handleUpdateResume}
            loading={updating}
          >
            更新简历
          </Button>
        </div>

        {profile?.resume_parsed_data && (
          <div>
            <Title level={4}>简历分析结果</Title>
            <Collapse>
              {renderAnalysisSection('技术能力分析', profile.resume_parsed_data.technical_analysis)}
              {renderAnalysisSection('工作经历分析', profile.resume_parsed_data.experience_analysis)}
              {renderAnalysisSection('教育背景分析', profile.resume_parsed_data.education_analysis)}
              {renderAnalysisSection('核心竞争力', profile.resume_parsed_data.core_competencies)}
              {renderAnalysisSection('职业倾向分析', profile.resume_parsed_data.career_analysis)}
            </Collapse>
          </div>
        )}
      </Card>

      <Card title="使用说明">
        <Paragraph>
          1. 在上方文本框中输入或粘贴您的简历内容
        </Paragraph>
        <Paragraph>
          2. 点击"更新简历"按钮，系统会自动进行深度分析
        </Paragraph>
        <Paragraph>
          3. 查看分析结果，了解您的优势和发展方向
        </Paragraph>
        <Paragraph>
          4. 前往"职位匹配"页面，获取个性化的职位推荐
        </Paragraph>
      </Card>
    </div>
  );
};

export default UserProfile;
