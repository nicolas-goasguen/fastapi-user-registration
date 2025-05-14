#!bin/bash

if [ "${RUN_TESTS}" == "true" ]; then
  pytest
else
  fastapi run main.py --port 80
fi
