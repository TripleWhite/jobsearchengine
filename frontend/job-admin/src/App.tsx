import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { Layout, Menu, Button, Space } from 'antd';
import { UserOutlined, LogoutOutlined } from '@ant-design/icons';
import JobList from './components/JobList';
import CreateJob from './components/CreateJob';
import JobDetail from './components/JobDetail';
import JobMatch from './components/JobMatch';
import UserProfile from './components/UserProfile';
import Login from './components/Login';
import { checkAuthStatus, logout } from './api/auth';
import { useEffect, useState } from 'react';

const { Header, Content } = Layout;

// 路由保护组件
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const auth = checkAuthStatus();
  if (!auth.isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
};

// 管理员路由保护组件
const AdminRoute = ({ children }: { children: React.ReactNode }) => {
  const auth = checkAuthStatus();
  if (!auth.isAuthenticated || !auth.isAdmin) {
    return <Navigate to="/jobs" replace />;
  }
  return <>{children}</>;
};

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [userEmail, setUserEmail] = useState<string | null>(null);

  useEffect(() => {
    const auth = checkAuthStatus();
    setIsAuthenticated(auth.isAuthenticated);
    setIsAdmin(auth.isAdmin);
    setUserEmail(auth.userEmail);
  }, []);

  return (
    <Router>
      <Layout className="layout" style={{ minHeight: '100vh' }}>
        <Header style={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'space-between',
          padding: '0 24px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div style={{ color: 'white', fontSize: '20px', marginRight: '30px' }}>
              职位管理系统
            </div>
            {isAuthenticated && (
              <Menu
                theme="dark"
                mode="horizontal"
                defaultSelectedKeys={['1']}
                items={[
                  {
                    key: '1',
                    label: '职位列表',
                    onClick: () => window.location.href = '/jobs'
                  },
                  {
                    key: '2',
                    label: '职位匹配',
                    onClick: () => window.location.href = '/match'
                  },
                  {
                    key: '3',
                    label: '个人资料',
                    onClick: () => window.location.href = '/profile'
                  }
                ]}
              />
            )}
          </div>
          
          <div>
            {isAuthenticated ? (
              <Space>
                <span style={{ color: 'white' }}>
                  <UserOutlined /> {userEmail}
                </span>
                <Button 
                  type="link" 
                  icon={<LogoutOutlined />}
                  onClick={logout}
                  style={{ color: 'white' }}
                >
                  退出
                </Button>
              </Space>
            ) : (
              <Button 
                type="link" 
                onClick={() => window.location.href = '/login'}
                style={{ color: 'white' }}
              >
                登录
              </Button>
            )}
          </div>
        </Header>
        
        <Content style={{ padding: '0 50px', marginTop: '16px' }}>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<Navigate to="/jobs" replace />} />
            <Route 
              path="/jobs" 
              element={
                <ProtectedRoute>
                  <JobList />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/jobs/create" 
              element={
                <AdminRoute>
                  <CreateJob />
                </AdminRoute>
              } 
            />
            <Route 
              path="/jobs/:id" 
              element={
                <ProtectedRoute>
                  <JobDetail />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/match" 
              element={
                <ProtectedRoute>
                  <JobMatch />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/profile" 
              element={
                <ProtectedRoute>
                  <UserProfile />
                </ProtectedRoute>
              } 
            />
          </Routes>
        </Content>
      </Layout>
    </Router>
  );
}

export default App;
