import React, { useEffect, useState } from 'react';
import { Table, Input, Space, Button } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import { getJobs, JobListResponse } from '../api/job';
import { useNavigate } from 'react-router-dom';

const { Search } = Input;

const JobList: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [jobList, setJobList] = useState<JobListResponse['jobs']>([]);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0,
  });
  const [searchTitle, setSearchTitle] = useState('');
  const [searchLocation, setSearchLocation] = useState('');
  const navigate = useNavigate();

  const fetchJobs = async (page = 1, title = searchTitle, location = searchLocation) => {
    setLoading(true);
    try {
      const response = await getJobs({
        job_title: title,
        location: location,
        page,
        per_page: pagination.pageSize,
      });
      setJobList(response.jobs);
      setPagination({
        ...pagination,
        current: response.pagination.current_page,
        total: response.pagination.total,
      });
    } catch (error) {
      console.error('Failed to fetch jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const columns = [
    {
      title: '职位名称',
      dataIndex: 'job_title',
      key: 'job_title',
      render: (text: string, record: any) => (
        <a onClick={() => navigate(`/jobs/${record.id}`)}>{text}</a>
      ),
    },
    {
      title: '公司',
      dataIndex: 'company_name',
      key: 'company_name',
    },
    {
      title: '地点',
      dataIndex: 'location',
      key: 'location',
    },
    {
      title: '发布时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (text: string) => new Date(text).toLocaleDateString(),
    },
  ];

  const handleTableChange = (pagination: any) => {
    fetchJobs(pagination.current);
  };

  const handleSearch = () => {
    fetchJobs(1, searchTitle, searchLocation);
  };

  return (
    <div style={{ padding: '24px' }}>
      <Space style={{ marginBottom: 16 }} size="large">
        <Search
          placeholder="搜索职位名称"
          allowClear
          style={{ width: 200 }}
          value={searchTitle}
          onChange={(e) => setSearchTitle(e.target.value)}
          onSearch={handleSearch}
        />
        <Search
          placeholder="搜索地点"
          allowClear
          style={{ width: 200 }}
          value={searchLocation}
          onChange={(e) => setSearchLocation(e.target.value)}
          onSearch={handleSearch}
        />
        <Button
          type="primary"
          icon={<SearchOutlined />}
          onClick={handleSearch}
        >
          搜索
        </Button>
        {localStorage.getItem('isAdmin') === 'true' && (
          <Button type="primary" onClick={() => navigate('/jobs/create')}>
            创建职位
          </Button>
        )}
      </Space>

      <Table
        columns={columns}
        dataSource={jobList}
        rowKey="id"
        pagination={pagination}
        loading={loading}
        onChange={handleTableChange}
      />
    </div>
  );
};

export default JobList;
