# Power Plants API

这是一个基于FastAPI的电站数据管理系统API，提供电站日报、月报和用户管理的增删改查功能。

## 功能特性

- 完整的CRUD API接口
- 自动生成的API文档（Swagger UI和ReDoc）
- 基于SQLAlchemy的ORM数据库操作
- 类型安全的Pydantic模型
- MySQL数据库支持
- 自动化部署脚本
- 日志管理
- 环境配置管理

## 技术栈

- Python 3.8+
- FastAPI
- SQLAlchemy
- Pydantic
- MySQL
- Uvicorn
- Nginx (生产环境)

## 项目结构
```plaintext
my_api_project/
├── alembic/ # 数据库迁移相关文件
├── app/
│ ├── init.py
│ ├── main.py # FastAPI应用主入口
│ ├── core/
│ │ ├── init.py
│ │ ├── config.py # 配置文件
│ │ └── database.py # 数据库连接配置
│ ├── models/ # SQLAlchemy模型
│ │ ├── init.py
│ │ ├── base.py # 模型基类
│ │ ├── user.py # 用户模型
│ │ ├── plant.py # 电站模型
│ │ ├── daily_report.py # 日报模型
│ │ └── monthly_report.py # 月报模型
│ ├── schemas/ # Pydantic模型
│ │ ├── init.py
│ │ ├── user.py # 用户模式
│ │ ├── daily_report.py # 日报模式
│ │ └── monthly_report.py # 月报模式
│ ├── crud/ # CRUD操作
│ │ ├── init.py
│ │ ├── base.py # 基础CRUD操作
│ │ ├── user.py # 用户CRUD
│ │ ├── daily_report.py # 日报CRUD
│ │ └── monthly_report.py # 月报CRUD
│ └── api/ # API路由
│ ├── deps.py # 依赖注入
│ └── v1/ # API版本1
│ ├── init.py
│ └── endpoints/ # API端点
├── config/ # 配置文件
│ ├── production.conf # 生产环境配置
│ └── logging.conf # 日志配置
├── requirements.txt # 项目依赖
├── run.py # 启动脚本
├── start.sh # 本地启动脚本
├── deploy.sh # 远程部署脚本
└── local_deploy.sh # 本地部署脚本
```
## 快速开始

### 开发环境设置

1. 克隆项目：
bash
git clone <repository-url>
cd power-plants-api

2. 安装依赖：

### 配置

1. 创建数据库配置文件：

bash:README.md
mkdir -p /opt/power-plants/config/
cp config/production.conf /opt/power-plants/config/database.conf

2. 修改数据库配置：

```ini
database.host=localhost
database.name=power_plants_db
database.user=power_plants_user
database.password=your_secure_password
```

## API 文档

启动服务后，可以通过以下地址访问API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 主要API端点

### 日报管理
- `GET /api/v1/daily-reports/` - 获取日报列表
- `POST /api/v1/daily-reports/` - 创建新日报
- `GET /api/v1/daily-reports/{report_id}` - 获取特定日报
- `PUT /api/v1/daily-reports/{report_id}` - 更新日报
- `DELETE /api/v1/daily-reports/{report_id}` - 删除日报
- `GET /api/v1/daily-reports/plant/{plant_id}` - 获取特定电站的日报
- `GET /api/v1/daily-reports/owner/{owner_id}` - 获取特定用户的日报

### 月报管理
- `GET /api/v1/monthly-reports/` - 获取月报列表
- `POST /api/v1/monthly-reports/` - 创建新月报
- `GET /api/v1/monthly-reports/{report_id}` - 获取特定月报
- `PUT /api/v1/monthly-reports/{report_id}` - 更新月报
- `DELETE /api/v1/monthly-reports/{report_id}` - 删除月报
- `GET /api/v1/monthly-reports/user/{user_id}` - 获取特定用户的月报
- `GET /api/v1/monthly-reports/date-range/` - 获取日期范围内的月报

### 用户管理
- `GET /api/v1/users/` - 获取用户列表
- `POST /api/v1/users/` - 创建新用户
- `GET /api/v1/users/active` - 获取活跃用户
- `GET /api/v1/users/{user_id}` - 获取特定用户
- `PUT /api/v1/users/{user_id}` - 更新用户
- `DELETE /api/v1/users/{user_id}` - 删除用户

## 部署

### 本地开发环境
```bash
./start.sh
```

### 生产环境部署
1. 修改 `local_deploy.sh` 中的配置：
```bash
REMOTE_HOST="us.wangjingfei.com"
REMOTE_USER="your_ssh_user"
```

2. 执行部署：
```bash
chmod +x local_deploy.sh
./local_deploy.sh
```

## 日志

日志文件位置：
- 应用日志: `/opt/power-plants/logs/app.log`
- 错误日志: `/opt/power-plants/logs/fastapi.error.log`
- Nginx访问日志: `/opt/power-plants/logs/nginx.access.log`

## 开发指南

1. 添加新的模型：
   - 在 `app/models/` 中创建新的SQLAlchemy模型
   - 在 `app/schemas/` 中创建对应的Pydantic模型
   - 在 `app/crud/` 中实现CRUD操作
   - 在 `app/api/v1/endpoints/` 中添加API路由

2. 数据库迁移：
   - 创建迁移脚本
   - 应用迁移到数据库

## 环境要求

- Python 3.8+
- MySQL 5.7+
- Nginx (生产环境)
- Linux/Unix 系统

## 许可证

[MIT License](LICENSE)

