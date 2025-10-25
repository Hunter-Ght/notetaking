# 笔记应用重构与部署计划

## 1. 环境准备

### 1.1. 安装新依赖
- 安装 `psycopg2-binary` 用于连接 PostgreSQL 数据库。
- 安装 `python-dotenv` 用于管理环境变量。
- 安装 `openai` 用于集成 GPT-4o-mini。
- 更新 `requirements.txt` 文件。

```bash
pip install psycopg2-binary python-dotenv openai
pip freeze > requirements.txt
```

### 1.2. 配置 `.env` 文件
- 创建 `.env` 文件用于存储敏感信息。
- 添加 Supabase 数据库 URL 和 OpenAI API Key。

```
# .env
DATABASE_URL="your_supabase_postgres_connection_string"
OPENAI_API_KEY="your_openai_api_key"
```

### 1.3. 更新 `.gitignore`
- 确保 `.env` 文件和 `__pycache__/` 目录被忽略，以防止敏感信息和临时文件被提交到版本库。

```
# .gitignore
.env
__pycache__/
*.pyc
database/
```

## 2. 数据库迁移：从 SQLite 到 Supabase Postgres

### 2.1. 创建 Supabase 项目
- 在 [Supabase](https://supabase.com/) 官网创建一个新项目。
- 获取数据库连接字符串 (Connection String) 并配置到 `.env` 文件中。

### 2.2. 定义表结构
- 在 Supabase SQL Editor 中创建 `notes` 表。

```sql
CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    translation TEXT,
    summary TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 2.3. 更新 CRUD 操作 (SQLAlchemy)
- 修改 `src/models/note.py` 和 `src/routes/note.py`。
- 更新数据库连接，使用从环境变量中加载的 `DATABASE_URL`。
- 确保所有 CRUD (Create, Read, Update, Delete) 操作都能在新的 Postgres 数据库上正常工作。

## 3. 代码重构

### 3.1. 加载环境变量
- 在 `src/main.py` 或相关配置文件中，使用 `python-dotenv` 加载 `.env` 文件中的环境变量。

```python
from dotenv import load_dotenv
import os

load_dotenv()

# Get variables
db_url = os.getenv("DATABASE_URL")
openai_api_key = os.getenv("OPENAI_API_KEY")
```

### 3.2. 集成 GPT-4o-mini
- 创建一个新的服务或模块用于处理与 OpenAI API 的交互。
- 实现笔记翻译和生成功能。

#### 翻译功能
- 在 `src/routes/note.py` 中添加一个新的路由，接收笔记 ID 和目标语言。
- 调用 OpenAI API (`gpt-4o-mini`) 进行翻译，并将结果存回数据库。

#### 笔记生成
- 添加一个路由，接收一个主题或提示。
- 使用 `gpt-4o-mini` 生成笔记内容并保存。

### 3.3. 兼容 Serverless 架构
- 将 Flask 应用的主入口文件 `src/main.py` 调整为 Vercel Serverless Functions 能够识别的格式。
- Vercel 会自动处理 Flask 应用的 `app` 对象。

## 4. 本地测试

### 4.1. 启动本地开发服务器
- 确保所有环境变量已正确加载。
- 运行应用。

```bash
conda activate notetaking
python src/main.py
```

### 4.2. 测试所有功能
- **CRUD 操作**: 增、删、改、查笔记。
- **翻译功能**: 测试笔记翻译是否成功。
- **生成功能**: 测试 AI 生成笔记是否正常。
- **数据库连接**: 确认数据已正确写入 Supabase 数据库。

## 5. Vercel 部署

### 5.1. 安装 Vercel CLI
```bash
npm install -g vercel
```

### 5.2. 配置 `vercel.json`
- 在项目根目录创建 `vercel.json` 文件，用于配置构建和路由规则。

```json
{
  "version": 2,
  "builds": [
    {
      "src": "src/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "src/main.py"
    }
  ]
}
```

### 5.3. 部署到 Vercel
- 登录 Vercel CLI。
- 在项目根目录运行 `vercel` 命令进行部署。
- 在 Vercel 项目设置中，添加 `DATABASE_URL` 和 `OPENAI_API_KEY` 环境变量。

```bash
vercel login
vercel
```

## 6. 可选独特功能

### 6.1. 笔记总结
- 类似于翻译功能，创建一个路由，接收笔记 ID。
- 调用 `gpt-4o-mini` 生成笔记内容的摘要。
- 将摘要保存到 `notes` 表的 `summary` 字段。

## 7. 实验报告 `lab2_writeup.md` 大纲

### 1. 项目概述
- 项目目标：重构笔记应用，集成 AI 功能，并迁移到云端。
- 技术栈：Python, Flask, SQLAlchemy, Supabase, OpenAI, Vercel。

### 2. 核心功能实现
- **数据库迁移**:
  - 从 SQLite 到 Supabase Postgres 的过程。
  - 表结构设计与挑战。
- **AI 功能集成**:
  - GPT-4o-mini 用于翻译和生成笔记的实现细节。
  - API 交互和错误处理。
- **云端部署**:
  - Vercel 部署流程。
  - Serverless 配置 (`vercel.json`)。
  - 环境变量管理。

### 3. 系统设计
- 架构图（重构前后对比）。
- 模块说明（例如 `routes`, `models`）。

### 4. 遇到的问题与解决方案
- 描述在开发过程中遇到的主要挑战（例如，数据库连接问题、依赖冲突、部署错误）。
- 详细说明如何解决这些问题。

### 5. 总结与展望
- 项目成果总结。
- 未来可以改进或扩展的功能（例如，用户认证、更丰富的 AI 功能）。