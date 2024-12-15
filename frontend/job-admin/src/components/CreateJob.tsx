import React, { useState } from 'react';
import { Form, Input, Button, Card, message } from 'antd';
import { createJob } from '../api/job';
import { useNavigate } from 'react-router-dom';

const { TextArea } = Input;

const CreateJob: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const onFinish = async (values: { raw_jd_text: string }) => {
    setLoading(true);
    try {
      const response = await createJob(values.raw_jd_text);
      message.success('职位创建成功！');
      navigate(`/jobs/${response.job_id}`);
    } catch (error: any) {
      message.error(error.response?.data?.error || '创建失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '24px', maxWidth: '800px', margin: '0 auto' }}>
      <Card title="创建新职位" bordered={false}>
        <Form
          layout="vertical"
          onFinish={onFinish}
        >
          <Form.Item
            label="职位描述文本"
            name="raw_jd_text"
            rules={[
              { required: true, message: '请输入职位描述文本' },
              { min: 50, message: '职位描述文本至少需要50个字符' }
            ]}
            extra="请粘贴完整的职位描述文本，系统将自动解析出职位名称、职责、要求等信息。"
          >
            <TextArea
              rows={15}
              placeholder="请在此粘贴完整的职位描述文本..."
              style={{ fontFamily: 'monospace' }}
            />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading} block>
              创建职位
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default CreateJob;
