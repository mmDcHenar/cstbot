FROM python:3.12-slim
LABEL authors="mmDcHenar"

ENV PYTHONUNBUFFERED 1

WORKDIR /src/

COPY requirements.txt .
RUN [ "pip", "install", "--upgrade", "--no-cache-dir", "-r", "requirements.txt" ]

COPY . .

RUN [ "python", "manage.py", "collectstatic", "--no-input" ]

CMD [ "bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000" ]
