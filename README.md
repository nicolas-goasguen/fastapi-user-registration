# User Registration API

This repository contains an implementation of API user registration and verification.

## Features

* Create a user with an email and a password.
* Email the user with a 4 digits code.
* Activate a user account with the 4 digits code received using basic authentication.
* The user has only one minute to use this code. An error is raised if used after that.

##          

## Architecture

### Docker services architecture

This backend project is structured in Docker services as follows:

- **FastAPI**: The Python backend API to handle user registration and activation.
- **PostgreSQL**: The SQL database to store users and verification data.
- **MailDev**: The SMTP testing service to simulate user email verification.
- **RabbitMQ**: The message broker used to queue asynchronous tasks.
- **Celery Worker**: The worker that processes background tasks from the queue.

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

### API code architecture

The application is organized in a modular way under the `src/` folder:

- **main.py**: Entry point to launch the FastAPI app.
- **auth/**: Contains utilities and dependencies related to authentication.
    - `utils.py`: Basic authentication helpers.
    - `dependencies.py`: FastAPI dependencies for authentication.
- **user/**: Manages user-related features.
    - `schemas.py`, `crud.py`, `router.py`, `service.py`, `tasks/email.py`, `exceptions.py`, `utils.py`: Complete user
      logic including email verification.
    - `tests/`: Extensive test coverage including unit, integration, functional and e2e layers.
- **workers/**: Celery worker configuration (`celery.py`).
- **config.py**, **database.py**, **exceptions.py**, **logging.py**, **dependencies.py**: Core configurations and shared
  infrastructure.

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

This layout separates concerns clearly and supports scalable testing and feature development.

## Setup

### Prerequisites

- Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).

### (Optional) Create a custom .env file

By default, the project uses the `.env.example` file. If needed, you can create a custom environment file.

```console
foo@bar:~$ cp .env.example <custom_env_file>
```

Then, open and modify the custom environment file to fit your needs.

## Usage

### Start the environment

> [!IMPORTANT]
> Ensure that your environment file is properly configured before running the app.

To start the application using the default configuration:

```console
foo@bar:~$ docker-compose --env-file .env.example up --build
```

Once running, access the services from your web browser:

- **API**: `http://localhost:<EXPOSED_API_PORT>/docs`
- **Mail**: `http://localhost:<EXPOSED_SMTP_WEB_PORT>`

<details>
  <summary>(Alternative) Command for custom environment file</summary>
  If you have created a custom environment file, specify it as follows:

  ```console
  foo@bar:~$ docker-compose --env-file <custom_env_file> up --build
  ```

</details>

### Run tests

> [!CAUTION]
> This will create random test data. Do NOT run in a production environment.

To run the tests on the environment:

```console
foo@bar:~$ docker-compose --env-file .env.example exec api pytest
```

You'll now see the logs of your running services in the terminal.

<details>
  <summary>(Alternative) Command for custom environment file</summary>
  If you have created a custom environment file, specify it as follows:

  ```console
  foo@bar:~$ docker-compose --env-file <custom_env_file> exec api pytest
  ```

</details>

### Stop the environment

To stop the running services:

```console
foo@bar:~$ docker-compose --env-file .env.example down
```

<details>
  <summary>(Alternative) Command for custom environment file</summary>
  If you have created a custom environment file, specify it as follows:

  ```console
  foo@bar:~$ docker-compose --env-file <custom_env_file> down
  ```

</details>

### Clean the environment

> [!CAUTION]
> This will erase all stored data. Do NOT run in a production environment.

To stop and remove persistent storage volumes:

```console
foo@bar:~$ docker-compose --env-file .env.example down -v
```

<details>
  <summary>(Alternative) Command for custom environment file</summary>
  If you have created a custom environment file, specify it as follows:

  ```console
  foo@bar:~$ docker-compose --env-file <custom_env_file> down -v
  ```

</details>

## Possible improvements

Here are some potential improvements for this project:

- **Documentation**: Add docstrings on schemas, methods, routes and returned values for API documentation.
- **Security**: Implement some advanced security strategies to protect against potential attacks (Timing Attack,
  DDoS, ...).

## License

The User Registration API is licensed under the terms of the MIT license.
