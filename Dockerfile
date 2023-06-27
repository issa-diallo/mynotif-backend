FROM python:3.11-slim as base

ARG PORT=8000
ENV PORT ${PORT}

WORKDIR /app

RUN apt update \
    && apt --yes --no-install-recommends install \
    make \
    && apt clean

COPY Makefile requirements.txt /app/
RUN make virtualenv
COPY src /app/src
RUN make run/collectstatic

FROM python:3.11-alpine
WORKDIR /app
COPY --from=base /app/venv/ /app/venv/
COPY src /app/src
COPY --from=base /app/src/staticfiles/ /app/src/staticfiles/

CMD ["/app/venv/bin/gunicorn", "--chdir", "src", "--bind", "0.0.0.0:8000", "main.wsgi"]
EXPOSE ${PORT}
