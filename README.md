# Job Management System

一个现代化的求职管理系统，使用 Flask + React 技术栈构建。

## 项目结构

```
.
├── app/                    # Flask 后端应用
│   ├── routes/            # API 路由
│   ├── services/          # 业务逻辑服务
│   └── models.py          # 数据库模型
├── frontend/              # 前端应用
│   └── job-admin/        # React 管理后台
├── migrations/            # 数据库迁移文件
├── tests/                 # 测试用例
├── .env                   # 环境变量配置
└── requirements.txt       # Python 依赖
```

## 技术栈

### 后端
- Python 3.x
- Flask 3.0.0
- SQLAlchemy
- Flask-Migrate
- Flask-CORS
- JWT 认证

### 前端
- React 18
- TypeScript
- Ant Design
- Vite
- React Router
- Axios

## 开发环境设置

### 后端设置

1. 创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Unix
# 或
.\venv\Scripts\activate  # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 设置环境变量：
```bash
# 创建 .env 文件并配置以下变量
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=sqlite:///instance/app.db
SECRET_KEY=your-secret-key
```

4. 初始化数据库：
```bash
flask db upgrade
```

5. 创建管理员账户：
```bash
python create_admin.py
```

6. 运行后端服务：
```bash
python run.py
```
服务将在 http://localhost:5001 运行

### 前端设置

1. 进入前端目录：
```bash
cd frontend/job-admin
```

2. 安装依赖：
```bash
npm install
```

3. 运行开发服务器：
```bash
npm run dev
```
前端将在 http://localhost:5173 运行

## 运行项目

### 数据库设置

1. 初始化数据库：
```bash
flask db upgrade
```

2. 创建管理员用户：
```bash
python3 create_admin.py
```

这将创建以下用户：
- 管理员账号：admin@example.com (密码: admin123)
- 测试用户账号：test@example.com (密码: test123)

### 后端服务器

1. 安装依赖：
```bash
python3 -m pip install -r requirements.txt
```

2. 运行后端服务器：
```bash
python3 run.py
```

服务器将在 http://localhost:5002 上运行。

### 前端应用

1. 进入前端目录：
```bash
cd frontend/job-admin
```

2. 安装依赖：
```bash
npm install
```

3. 运行开发服务器：
```bash
npm run dev
```

前端应用将在 http://localhost:5173 上运行。

## 测试

运行测试套件：
```bash
pytest
```

生成测试覆盖率报告：
```bash
pytest --cov=app tests/
```

## API 文档

### 认证相关
- POST /api/auth/login - 用户登录
- POST /api/auth/register - 用户注册

### 职位相关
- GET /api/jobs - 获取职位列表
- POST /api/jobs - 创建新职位
- GET /api/jobs/{id} - 获取职位详情
- PUT /api/jobs/{id} - 更新职位信息
- DELETE /api/jobs/{id} - 删除职位

### 用户相关
- GET /api/users/profile - 获取用户信息
- PUT /api/users/profile - 更新用户信息

## 部署

1. 构建前端：
```bash
cd frontend/job-admin
npm run build
```

2. 配置生产环境变量：
```bash
FLASK_ENV=production
DATABASE_URL=your-production-db-url
SECRET_KEY=your-production-secret-key
```

3. 运行数据库迁移：
```bash
flask db upgrade
```

4. 使用生产服务器（如 Gunicorn）运行应用：
```bash
gunicorn run:app
```

## 贡献指南

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情
