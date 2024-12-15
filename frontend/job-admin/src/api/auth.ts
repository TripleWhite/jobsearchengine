import axios from 'axios';

const API_BASE_URL = 'http://localhost:5002/api';

export interface LoginResponse {
  status: string;
  token: string;
  user: {
    id: number;
    email: string;
    name: string;
    is_admin: boolean;
  };
}

export const login = async (email: string, password: string): Promise<LoginResponse> => {
  const response = await axios.post(`${API_BASE_URL}/auth/login`, {
    email,
    password,
  });
  return response.data;
};

export const checkAuthStatus = () => {
  const token = localStorage.getItem('token');
  const isAdmin = localStorage.getItem('isAdmin') === 'true';
  const userEmail = localStorage.getItem('userEmail');
  return {
    isAuthenticated: !!token,
    isAdmin,
    userEmail,
  };
};

export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('isAdmin');
  localStorage.removeItem('userEmail');
  window.location.href = '/login';
};
