FROM python:3.11-alpine as base

WORKDIR /app

RUN apk add --update --no-cache \
    make

COPY Makefile requirements.txt /app/
RUN make virtualenv
COPY src /app/src
RUN make run/collectstatic


FROM python:3.11-alpine

ARG PORT=8000
ARG VERSION
ENV PORT ${PORT}
ENV VERSION ${VERSION}
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY --from=base /app/venv/ /app/venv/
COPY src /app/src
COPY --from=base /app/src/staticfiles/ /app/src/staticfiles/

CMD ["sh", "-c", "/app/venv/bin/gunicorn --chdir src --bind 0.0.0.0:${PORT} main.wsgi"]
EXPOSE ${PORT}
