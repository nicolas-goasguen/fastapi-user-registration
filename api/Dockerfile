FROM python:3.11

WORKDIR /src
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
COPY src /src

CMD ["fastapi", "run", "main.py", "--port", "80"]
