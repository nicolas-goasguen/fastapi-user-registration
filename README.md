# User Registration API

This repository provides an API for user registration and email verification using FastAPI.

## Features

- Register a user with email and password
- Send a 4-digit verification code via email
- Activate a user account using HTTP Basic Auth with the received code
- The verification code is valid for 1 minute only

## Architecture

### Docker Services

This project is structured into the following Docker services:

- **FastAPI**: Handles HTTP requests and business logic
- **PostgreSQL**: Stores user and verification data
- **MailDev**: Simulates an SMTP email server
- **RabbitMQ**: Message broker for background tasks
- **Celery Worker**: Processes asynchronous tasks

```mermaid
architecture-beta
    service localhost(server)[Host]

    group docker_compose[Docker Compose]
    service api(server)[FastAPI] in docker_compose
    service db(database)[PostgreSQL] in docker_compose
    service email(server)[MailDev] in docker_compose
    service broker(queue)[RabbitMQ] in docker_compose
    service worker(worker)[Celery Worker] in docker_compose
    junction junction_host_email

    localhost:R <--> L:api

    api:B <--> T:db

    api:R --> L:broker
    broker:T --> B:worker
    worker:L --> R:email

    email:L -- R:junction_host_email
    junction_host_email:B --> T:localhost
    localhost:T <-- B:junction_host_email    
```

### Codebase Structure

The application follows a modular layout inside `src/`:

- `main.py`: FastAPI app entry point
- `auth/`: Authentication-related utilities and dependencies
- `user/`: User logic including schemas, service, tasks, and routes
- `workers/`: Celery configuration
- Shared modules: `config.py`, `database.py`, `exceptions.py`, `logging.py`

```mermaid
graph TD;
    subgraph src/
        main[main.py] --> app[FastAPI app]

        app --> auth
        auth --> utils_auth[utils.py]
        auth --> deps_auth[dependencies.py]

        app --> user
        user --> router_user[router.py]
        user --> service_user[service.py]
        user --> crud_user[crud.py]
        user --> schemas_user[schemas.py]
        user --> tasks_user[tasks/email.py]

        app --> workers
        workers --> celery[celery.py]

        app --> shared_config[config.py]
        app --> shared_db[database.py]
        app --> shared_exceptions[exceptions.py]
        app --> shared_logging[logging.py]
    end
```

## Setup

### Prerequisites

Make sure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Environment File

You can use the default `.env.example` file in the following steps or create your custom environment file:

```bash
cp .env.example <your-env-file>
```

> You can modify the file according to your needs, and create a file for each environment
> (for example: development and production)

⚠️ **Important**: Docker Compose loads the environment file automatically if it's named `.env`.  
If your environment file has a different name, you must include it explicitly in each command, for example:

```bash
docker compose --env-file <your-env-file> up --build
```

## Usage

### Start in Development Mode (with override)

Use the default `docker-compose.override.yml` to enable volume mounting and code reload:

```bash
docker compose --env-file <your-env-file> up --build
```

In this mode, the override compose file allows the server to watch your code and restarts automatically on changes.

### Start in Production Mode (without override)

This only uses `docker-compose.yml`, ignoring the override file:

```bash
docker compose --env-file <your-env-file> -f docker-compose.yml up --build
```

### Accessing the Services

- **API Docs**: http://localhost:<EXPOSED_API_PORT>/docs
- **MailDev UI**: http://localhost:<EXPOSED_SMTP_WEB_PORT>

## Running Tests

```bash
docker compose exec api pytest
```

## Cleanup

### Stop all services

```bash
docker compose down
```

### Remove all volumes (irreversible)

```bash
docker compose down -v
```

## Possible Improvements

- Add docstrings to models, endpoints, and services for better documentation.
- Improve security (e.g., timing attack protection, request throttling).

## License

MIT
