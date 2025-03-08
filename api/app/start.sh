#!bin/bash

if [ "${ENVIRONMENT}" == "prod" ]; then
  fastapi run main.py --port 80
elif [ "${ENVIRONMENT}" == "test" ]; then
  pytest --asyncio-mode=auto
else
  echo "Unknown ENVIRONMENT: ${ENVIRONMENT}. Please set your ENVIRONMENT variable to 'prod' or 'test'."
  exit 1
fi
