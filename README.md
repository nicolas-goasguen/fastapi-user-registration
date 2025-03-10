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

```mermaid
architecture-beta
    service localhost(server)[Host]
  
    group docker_compose[Docker Compose]
    service api(server)[FastAPI] in docker_compose
    service db(database)[PostgreSQL] in docker_compose
    service email(server)[MailDev] in docker_compose
    junction junction_host_email

    api:R <--> L:db
    api:B --> T:email
    
    localhost:R <--> L:api
    localhost:B <-- T:junction_host_email
    junction_host_email:R -- L:email
```

### API code architecture

The API code is structured in multiple modules:
- main: Entry point that imports core modules and runs the FastAPI app.
- core: Contains essential components like configuration, database connection, and utilities.
- routers: Contains API routes, including user routes.
- schemas: Contains API models, including user schemas.
- services: Handles business logic, such as user services. Services are called by routes.

```mermaid
graph TD;
    subgraph API code structure
        main -->|Imports| core
        core --> config
        core --> db
        core --> utils

        main -->|Runs| app
        app -->|Defines routers| routers
        routers -->|Define endpoints| users_routes[routers/users]
        schemas -->|Define schemas| users_schemas[schemas/users]
        users_routes -->|Use schemas| users_schemas
        users_routes <-->|Calls services| users_services
        services -->|Define services| users_services[services/users]
    end
```

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
- **Validation**: Add much more validation for emails and passwords (at both database and schemas levels).
- **Add models**: Use models to manage database CRUD for a cleaner architecture.
- **Documentation**: Add docstrings on schemas, methods, routes and returned values for API documentation.
- **Error handling**: Improve error management in routes, especially for database connection failures.
- **Testing coverage**: Improve test coverage with more cases (including data validation).
- **Security**: Implement some advanced strategies to protect against potential attacks (Timing Attack, DDoS, ...).

## License
The User Registration API is licensed under the terms of the MIT license.
