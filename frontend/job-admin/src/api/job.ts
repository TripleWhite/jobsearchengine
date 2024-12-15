import axios from 'axios';

const API_BASE_URL = 'http://localhost:5002/api';

// 设置 axios 默认配置
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  config.headers['Content-Type'] = 'application/json';
  config.withCredentials = true;  // 添加这个配置以支持跨域请求携带凭证
  return config;
});

export interface Job {
  id: number;
  job_title: string;
  company_name: string;
  location: string;
  responsibilities: string[];
  requirements: string[];
  raw_jd_text: string;
  created_at: string;
  updated_at: string;
}

export interface JobListResponse {
  status: string;
  jobs: {
    id: number;
    job_title: string;
    company_name: string;
    location: string;
    created_at: string;
  }[];
  pagination: {
    total: number;
    pages: number;
    current_page: number;
    per_page: number;
    has_next: boolean;
    has_prev: boolean;
  };
}

export interface CreateJobResponse {
  status: string;
  job_id: number;
  message: string;
  job: Job;
}

export interface JobRecommendation {
  job_id: number;
  match_score: number;
  match_analysis: string;
  advantages: string[];
  challenges: string[];
  suggestions: string[];
  job_details: Job;
}

export interface MatchJobsResponse {
  status: string;
  recommendations: JobRecommendation[];
  message?: string;
}

// 创建新职位
export const createJob = async (rawJdText: string): Promise<CreateJobResponse> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/job/admin/create_job`, {
      raw_jd_text: rawJdText,
    });
    return response.data;
  } catch (error: any) {
    console.error('Create job error:', error.response || error);
    throw error;
  }
};

// 获取职位列表
export const getJobs = async (params: {
  job_title?: string;
  location?: string;
  page?: number;
  per_page?: number;
}): Promise<JobListResponse> => {
  const response = await axios.get(`${API_BASE_URL}/job`, { params });
  return response.data;
};

// 获取职位详情
export const getJobById = async (jobId: number): Promise<{ status: string; job: Job }> => {
  const response = await axios.get(`${API_BASE_URL}/job/${jobId}`);
  return response.data;
};

// 匹配职位
export const matchJobs = async (params: {
  desired_position: string;
  desired_location: string;
}): Promise<MatchJobsResponse> => {
  const response = await axios.get(`${API_BASE_URL}/job/match`, { params });
  return response.data;
};
