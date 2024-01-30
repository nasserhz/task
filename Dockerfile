FROM python:3.12-alpine3.19

RUN echo "https://uk.alpinelinux.org/alpine/v3.19/main" > /etc/apk/repositories ; \
    echo "https://uk.alpinelinux.org/alpine/v3.19/community" >> /etc/apk/repositories ;

ENV HOME=/home/app

RUN mkdir -p $HOME

WORKDIR $HOME

RUN addgroup -S app && adduser -S app -G app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libpq

RUN pip install poetry
COPY ./poetry.lock .
COPY ./pyproject.toml .
RUN poetry install

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g'  /home/app/entrypoint.sh
RUN chmod +x /home/app/entrypoint.sh

COPY . /home/app

RUN chown -R app:app /home/app

USER app

ENTRYPOINT ["/home/app/entrypoint.sh"]
