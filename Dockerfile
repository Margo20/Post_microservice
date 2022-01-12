FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Additional dependencies
  && apt-get install -y telnet netcat \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt


COPY ./entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./dockers/start-fastapi.sh /start-fastapi.sh
RUN sed -i 's/\r$//g' /start-fastapi.sh
RUN chmod +x /start-fastapi.sh

COPY ./dockers/start-celeryworker.sh /start-celeryworker.sh
RUN sed -i 's/\r$//g' /start-celeryworker.sh
RUN chmod +x /start-celeryworker.sh

COPY ./dockers/start-flower.sh /start-flower.sh
RUN sed -i 's/\r$//g' /start-flower.sh
RUN chmod +x /start-flower.sh

COPY ./dockers/start-consumer.sh /start-consumer.sh
RUN sed -i 's/\r$//g' /start-consumer.sh
RUN chmod +x /start-consumer.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]

