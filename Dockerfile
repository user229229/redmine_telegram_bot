FROM python:3.8-slim AS bot

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

# Env vars
ENV TELEGRAM_TOKEN ${TELEGRAM_TOKEN}
ENV PROJECT_ID ${PROJECT_ID}
ENV REDMINE_URL ${REDMINE_URL}
ENV REDMINE_KEY ${REDMINE_KEY}

RUN apt-get update
RUN apt-get install -y python3 python3-pip python-dev build-essential python3-venv

RUN mkdir -p /codebase /storage
ADD . /codebase
WORKDIR /codebase

RUN pip3 install -r requirements.txt
RUN chmod +x /codebase/bot.py

CMD python3 /codebase/bot.py;
