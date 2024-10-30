<p align="left">
    <a href="README.md">English</a> ｜ 中文
</p>

# FastAPI Backend Project

这是一个基于 **FastAPI** 框架的后端项目，数据库使用`MongoDB`，采用 `Docker` 和 `docker-compose` 进行管理，并通过 `Traefik` 作为反向代理进行负载均衡。本项目结构包含应用的 API、数据模型、CRUD 操作、依赖配置、用户认证和安全设置等模块，适用于开发和生产环境。

## 目录结构
```
.
├── README.md                   # 项目说明
├── backend                     # 后端应用代码和配置
│   ├── Dockerfile              # 后端 Docker 镜像构建文件
│   ├── app                     # FastAPI 应用目录
│   │   ├── api                 # API 路由和依赖配置
│   │   │   ├── endpoints       # API 路由定义
│   │   ├── core                # 核心配置和安全设置
│   │   ├── crud                # 数据库 CRUD 操作
│   │   ├── models              # 数据库模型定义
│   │   ├── schemas             # 数据传输模型定义
│   │   ├── utils               # 实用工具模块
│   │   └── main.py             # FastAPI 应用主入口
│   ├── gunicorn_conf.py        # Gunicorn 配置文件
│   └── scripts                 # 启动脚本
├── docker-compose.yml          # Docker Compose 配置文件
├── docker-compose.traefik.yml  # Docker Compose 配置文件（Traefik）
├── poetry.lock                 # Poetry 锁文件
├── pyproject.toml              # Poetry 项目配置文件
├── run.sh                      # 应用启动脚本
├── run.traefik.sh              # 使用 Traefik 启动的脚本
└── tests                       # 测试代码目录
```

## 功能

- **API 端点**：提供用户注册、登录、获取信息等接口。
- **用户认证**：支持 JWT 令牌的认证与授权。
- **CRUD 操作**：封装了数据操作的基本功能。
- **反向代理**：利用 Traefik 进行服务的动态路由和负载均衡。
- **配置管理**：Gunicorn 用于生产环境的应用部署。
- **测试支持**：包含测试文件，便于扩展自动化测试。

## 部署与运行

### 本地运行（无 Traefik）

```bash
# 启动 Docker 服务
./run.sh
```

### 使用 Traefik 部署

```bash
# 启动 Docker 服务（Traefik 支持）
./run.traefik.sh
```

### 配置说明

### Docker 环境变量

配置位于 .env 文件中，包含以下参数：

- **DB_URL**：数据库连接 URL
- **SECRET_KEY：JWT** 加密密钥
- **ALGORITHM**：JWT 加密算法
- **ACCESS_TOKEN_EXPIRE_MINUTES**：访问令牌过期时间（分钟）

Traefik 反向代理

使用 docker-compose.traefik.yml 配置文件，通过 Traefik 管理服务路由。将应用部署在 docker network 中，方便其他容器访问。