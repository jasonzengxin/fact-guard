# FactGuard - AI驱动的事实核查助手

FactGuard 是一个基于 AI 的事实核查工具，它可以帮助用户验证文本或网页内容的真实性。项目使用 FastAPI 作为后端，React 作为前端，提供了现代化的用户界面和高效的事实核查功能。

## 项目结构

```
fact-guard/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   └── services/       # 业务逻辑
│   ├── requirements.txt    # Python 依赖
│   └── main.py            # 后端入口
├── frontend/               # React 前端
│   ├── public/
│   ├── src/
│   │   ├── components/    # React 组件
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

## 技术栈

### 后端
- Python 3.8+
- FastAPI
- OpenAI API
- uvicorn

### 前端
- React 18
- Tailwind CSS
- Font Awesome
- Animate.css

## 开发环境设置

1. 克隆项目
```bash
git clone https://github.com/yourusername/fact-guard.git
cd fact-guard
```

2. 设置后端
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows

# 安装依赖
cd backend
pip install -r requirements.txt

# 设置环境变量
export OPENAI_API_KEY=your_api_key  # Linux/Mac
# 或
set OPENAI_API_KEY=your_api_key  # Windows
```

3. 设置前端
```bash
cd frontend
npm install
```

## 开发模式运行

1. 启动后端服务
```bash
cd backend
uvicorn main:app --reload --port 8000
```

2. 启动前端开发服务器（新终端）
```bash
cd frontend
npm start
```

现在你可以访问：
- 前端开发服务器：http://localhost:3000
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

## 生产环境部署

### 方法 1：使用 Docker Compose（推荐）

1. 确保安装了 Docker 和 Docker Compose

2. 构建和运行容器
```bash
docker-compose up --build
```

### 方法 2：独立部署

1. 构建前端
```bash
cd frontend
npm run build
```

2. 将构建后的文件复制到后端的静态文件目录
```bash
cp -r build/* ../backend/app/static/
```

3. 启动后端服务
```bash
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## 环境变量配置

创建 `.env` 文件在项目根目录：

```env
# Backend
OPENAI_API_KEY=your_api_key
DEBUG=False
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

## API 文档

API 文档使用 Swagger UI 自动生成，可在运行后端服务后访问：
- Swagger UI：http://localhost:8000/docs
- ReDoc：http://localhost:8000/redoc

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情 