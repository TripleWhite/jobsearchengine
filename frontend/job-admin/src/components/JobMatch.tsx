import React, { useState } from 'react';
import { matchJobs, JobRecommendation } from '../api/job';
import { Card, Input, Button, List, Typography, Spin, message, Progress, Tag, Collapse } from 'antd';

const { Title, Text, Paragraph } = Typography;
const { Panel } = Collapse;

const JobMatch: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState<JobRecommendation[]>([]);
  const [desiredPosition, setDesiredPosition] = useState('');
  const [desiredLocation, setDesiredLocation] = useState('');

  const handleMatch = async () => {
    if (!desiredPosition || !desiredLocation) {
      message.error('请输入期望职位和地点');
      return;
    }

    setLoading(true);
    try {
      const response = await matchJobs({
        desired_position: desiredPosition,
        desired_location: desiredLocation,
      });

      if (response.status === 'ok') {
        setRecommendations(response.recommendations);
        if (response.recommendations.length === 0) {
          message.info('未找到匹配的职位');
        }
      } else {
        message.error(response.message || '匹配失败');
      }
    } catch (error) {
      message.error('请求失败，请确保已上传简历');
    } finally {
      setLoading(false);
    }
  };

  const renderMatchDetails = (recommendation: JobRecommendation) => (
    <div>
      <div style={{ marginBottom: '16px' }}>
        <Progress
          percent={recommendation.match_score}
          status="active"
          strokeColor={{
            '0%': '#108ee9',
            '100%': '#87d068',
          }}
        />
      </div>

      <Collapse>
        <Panel header="匹配分析" key="1">
          <Paragraph>{recommendation.match_analysis}</Paragraph>
        </Panel>

        <Panel header="匹配优势" key="2">
          <List
            dataSource={recommendation.advantages}
            renderItem={item => (
              <List.Item>
                <Tag color="green">{item}</Tag>
              </List.Item>
            )}
          />
        </Panel>

        <Panel header="潜在挑战" key="3">
          <List
            dataSource={recommendation.challenges}
            renderItem={item => (
              <List.Item>
                <Tag color="orange">{item}</Tag>
              </List.Item>
            )}
          />
        </Panel>

        <Panel header="入职建议" key="4">
          <List
            dataSource={recommendation.suggestions}
            renderItem={item => (
              <List.Item>
                <Tag color="blue">{item}</Tag>
              </List.Item>
            )}
          />
        </Panel>

        <Panel header="职位详情" key="5">
          <List>
            <List.Item>
              <Text strong>职位要求：</Text>
              <ul>
                {recommendation.job_details.requirements.map((req, index) => (
                  <li key={index}>{req}</li>
                ))}
              </ul>
            </List.Item>
            <List.Item>
              <Text strong>工作职责：</Text>
              <ul>
                {recommendation.job_details.responsibilities.map((resp, index) => (
                  <li key={index}>{resp}</li>
                ))}
              </ul>
            </List.Item>
          </List>
        </Panel>
      </Collapse>
    </div>
  );

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>职位匹配</Title>
      
      <Card style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', gap: '16px', marginBottom: '16px' }}>
          <Input
            placeholder="期望职位（如：后端工程师）"
            value={desiredPosition}
            onChange={(e) => setDesiredPosition(e.target.value)}
            style={{ flex: 1 }}
          />
          <Input
            placeholder="期望地点（如：北京）"
            value={desiredLocation}
            onChange={(e) => setDesiredLocation(e.target.value)}
            style={{ flex: 1 }}
          />
          <Button type="primary" onClick={handleMatch} loading={loading}>
            开始匹配
          </Button>
        </div>
        
        <Paragraph type="secondary">
          提示：请先在个人资料页面上传简历，系统将根据您的简历信息为您推荐最匹配的职位。
        </Paragraph>
      </Card>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <Spin size="large" />
          <div style={{ marginTop: '16px' }}>正在进行智能匹配分析...</div>
        </div>
      ) : (
        <List
          dataSource={recommendations}
          renderItem={(item) => (
            <List.Item>
              <Card style={{ width: '100%' }}>
                <div style={{ marginBottom: '16px' }}>
                  <Title level={4}>{item.job_details.job_title}</Title>
                  <Text type="secondary">
                    {item.job_details.company_name} | {item.job_details.location}
                  </Text>
                </div>
                
                {renderMatchDetails(item)}
              </Card>
            </List.Item>
          )}
        />
      )}
    </div>
  );
};

export default JobMatch;
