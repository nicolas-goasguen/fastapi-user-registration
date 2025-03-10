# User Registration API
This repository contains an implementation of API user registration and verification.


## Features
* Create a user with an email and a password.
* Email the user with a 4 digits code.
* Activate a user account with the 4 digits code received with basic authentication.
* The user has only one minute to use this code. After that, an error should is raised.


## Architecture
This backend project is structured in Docker services as follows:
- **FastAPI**: the Python backend API to handle users registration and activation.
- **PostgreSQL**: the SQL database to store users and verification data.
- **MailDev**: the SMTP testing service to simulate user email verification.


## Setup and usage

### Prerequisites

- Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).


### (Optional) Create a custom .env file

Create a new `.env.<environment>` file from the `.env.example` file.

```shell
cp .env.example .env.<environment>
```

The file should be structured as follows, with some environment variables to customize:

```ini
# Project
PROJECT_NAME="User Registration API"  # <-- customize the name of the project 
ENVIRONMENT=example  # <-- customize the name of the environment
RUN_TESTS=false  # <-- set to 'true' to run the tests instead of the API (explained later) 

# Docker
EXPOSED_API_PORT=8000  # <-- change this to specify the port for the web access to the API on the host
EXPOSED_SMTP_WEB_PORT=1025  # <-- change this to specify the port for the web access to the MAIL service on the host

# Postgres
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=user_registration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=changethis  # <-- change this for better security

# API
DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:${POSTGRES_PORT}/${POSTGRES_DB}

# SMTP
SMTP_PORT=1025
SMTP_WEB_PORT=1080
SMTP_USER=admin
SMTP_PASSWORD=changethis  # <-- change this for better security
```


### Start the environment

Use your custom `.env.<environment>` file or the default `.env.example` file to run the app.

> [!IMPORTANT]
> Ensure that your .env file is properly configured before running the app.

```shell
docker-compose --env-file <env_file> up --build -d
```


Depending on your .env settings:
- API is accessible via FastAPI at `http://localhost:<EXPOSED_API_PORT>/docs`.
- Verification emails are accessible via MailDev at `http://localhost:<EXPOSED_SMTP_WEB_PORT>`.

For any issue, or just for monitoring purpose check the API logs with:

```shell
docker-compose --env-file <env_file> logs -f api
```

### Test an environment

Use your custom `.env.<environment>` file or the default `.env.example` file to run the tests on the previously created environment. Tests will validate user registration, email sending, email verification, and error handling.

> [!CAUTION]
> Do NOT run the tests on a production environment as it will create some random records and emails.

```shell
docker-compose --env-file <env_file> exec api pytest
```


### Stop

Use the following command to stops the services.

```sh
docker-compose --env-file <env_file> down -v
```


### Clean the environment

Use the following command to stops and remove the created volumes used for persistent storage.

> [!CAUTION]
> Do NOT run this on a production environment as it will erase the persistent data.

```sh
docker-compose --env-file <env_file> down -v
```


## License

The User Registration API is licensed under the terms of the MIT license.

