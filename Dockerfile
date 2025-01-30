FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get -y install cron openssh-client
RUN pip install poetry

WORKDIR /app
# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock ./

# Installing requirements
RUN poetry install --only main

COPY . .
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab

RUN /usr/bin/crontab /etc/cron.d/crontab

# run crond as main process of container
CMD ["cron", "-f"]