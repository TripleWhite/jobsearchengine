import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Descriptions, List, Button, Spin, message } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { getJobById, Job } from '../api/job';

const JobDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [job, setJob] = useState<Job | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchJob = async () => {
      if (!id) return;
      try {
        const response = await getJobById(parseInt(id));
        setJob(response.job);
      } catch (error) {
        message.error('获取职位详情失败');
        console.error('Failed to fetch job details:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchJob();
  }, [id]);

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!job) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        职位不存在
      </div>
    );
  }

  return (
    <div style={{ padding: '24px', maxWidth: '1000px', margin: '0 auto' }}>
      <Button
        icon={<ArrowLeftOutlined />}
        style={{ marginBottom: '16px' }}
        onClick={() => navigate('/jobs')}
      >
        返回列表
      </Button>

      <Card title={job.job_title} bordered={false}>
        <Descriptions column={2}>
          <Descriptions.Item label="公司名称">{job.company_name}</Descriptions.Item>
          <Descriptions.Item label="工作地点">{job.location}</Descriptions.Item>
          <Descriptions.Item label="发布时间">
            {new Date(job.created_at).toLocaleDateString()}
          </Descriptions.Item>
        </Descriptions>

        <Card
          type="inner"
          title="职位职责"
          style={{ marginTop: '24px' }}
        >
          <List
            dataSource={job.responsibilities}
            renderItem={(item) => (
              <List.Item>
                {item}
              </List.Item>
            )}
          />
        </Card>

        <Card
          type="inner"
          title="职位要求"
          style={{ marginTop: '24px' }}
        >
          <List
            dataSource={job.requirements}
            renderItem={(item) => (
              <List.Item>
                {item}
              </List.Item>
            )}
          />
        </Card>

        {localStorage.getItem('isAdmin') === 'true' && (
          <Card
            type="inner"
            title="原始JD文本"
            style={{ marginTop: '24px' }}
          >
            <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>
              {job.raw_jd_text}
            </pre>
          </Card>
        )}
      </Card>
    </div>
  );
};

export default JobDetail;
