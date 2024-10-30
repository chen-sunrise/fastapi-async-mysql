<p align="left">
    English | <a href="README.md">中文</a>
</p>

# FastAPI Backend Project

This is a FastAPI-based backend project using MongoDB as the database, managed by Docker and docker-compose, with Traefik acting as a reverse proxy and load balancer. The project structure includes API, data models, CRUD operations, dependency management, user authentication, and security settings, designed for both development and production environments.

## Project Structure
```
.
├── README.md                   # Project description
├── backend                     # Backend app code and configurations
│   ├── Dockerfile              # Dockerfile for backend image
│   ├── app                     # FastAPI application directory
│   │   ├── api                 # API routes and dependencies
│   │   │   ├── endpoints       # API endpoint definitions
│   │   ├── core                # Core configurations and security settings
│   │   ├── crud                # CRUD operations for the database
│   │   ├── models              # Database models
│   │   ├── schemas             # Data transfer schemas
│   │   ├── utils               # Utility modules
│   │   └── main.py             # Main entry for FastAPI application
│   ├── gunicorn_conf.py        # Gunicorn configuration
│   └── scripts                 # Startup scripts
├── docker-compose.yml          # Docker Compose configuration
├── docker-compose.traefik.yml  # Docker Compose config with Traefik
├── poetry.lock                 # Poetry lock file
├── pyproject.toml              # Poetry project config file
├── run.sh                      # Application startup script
├── run.traefik.sh              # Traefik-enabled startup script
└── tests                       # Test code directory
```

## Features

- **API Endpoints**: Provides user registration, login, and profile retrieval.
- **User Authentication**: JWT-based authentication and authorization.
- **CRUD Operations**: Encapsulated data manipulation functions.
- **Reverse Proxy**: Traefik-enabled dynamic routing and load balancing.
- **Configuration Management**: Gunicorn setup for production deployments.
- **Testing Support**: Ready for extended automated testing.

## Deployment and Running

### Local Run (without Traefik)

```bash
# Start Docker service
./run.sh
```

### Deployment with Traefik

```bash
# Start Docker service with Traefik support
./run.traefik.sh
```

### Configuration Guide

### Docker Environment Variables

Configured in the .env file, including:

- **DB_URL**: Database connection URL
- **SECRET_KEY**: Secret key for JWT encryption
- **ALGORITHM**: JWT encryption algorithm
- **ACCESS_TOKEN_EXPIRE_MINUTES**: Expiration time for access tokens (minutes)

### Traefik Reverse Proxy

Use the docker-compose.traefik.yml configuration file for Traefik, managing dynamic routing within the Docker network to ensure container accessibility across services.
