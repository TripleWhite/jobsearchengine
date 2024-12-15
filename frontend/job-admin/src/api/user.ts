import axios from 'axios';

const API_BASE_URL = 'http://localhost:5001/api';

export interface TechnicalAnalysis {
  tech_stack?: string[];
  depth_evaluation?: string;
  learning_ability?: string;
  practical_experience?: string;
}

export interface ExperienceAnalysis {
  years?: number;
  career_path?: string;
  project_highlights?: string[];
  problem_solving?: string;
}

export interface EducationAnalysis {
  background?: string;
  knowledge_base?: string;
  continuous_learning?: string;
}

export interface CoreCompetencies {
  key_skills?: string[];
  unique_strengths?: string;
  soft_skills?: string[];
}

export interface CareerAnalysis {
  suitable_positions?: string[];
  potential_fields?: string[];
  development_suggestions?: string;
  challenges?: string;
}

export interface ResumeParsedData {
  technical_analysis?: TechnicalAnalysis;
  experience_analysis?: ExperienceAnalysis;
  education_analysis?: EducationAnalysis;
  core_competencies?: CoreCompetencies;
  career_analysis?: CareerAnalysis;
}

export interface UserProfile {
  id: number;
  email: string;
  name: string | null;
  resume_text: string | null;
  resume_parsed_data: ResumeParsedData | null;
}

export interface ProfileResponse {
  status: string;
  user: UserProfile;
}

export interface UpdateResumeResponse {
  status: string;
  message: string;
  parsed_data?: ResumeParsedData;
}

// 获取用户资料
export const getProfile = async (): Promise<ProfileResponse> => {
  const response = await axios.get(`${API_BASE_URL}/user/profile`);
  return response.data;
};

// 更新简历
export const updateResume = async (resumeText: string): Promise<UpdateResumeResponse> => {
  const response = await axios.put(`${API_BASE_URL}/user/update_resume`, {
    resume_text: resumeText,
  });
  return response.data;
};

// 手动触发简历解析
export const parseResume = async (): Promise<UpdateResumeResponse> => {
  const response = await axios.post(`${API_BASE_URL}/user/parse_resume`);
  return response.data;
};
