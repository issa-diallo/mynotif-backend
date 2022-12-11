FROM python:3.9-slim

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

CMD ["make", "run/prod"]
EXPOSE ${PORT}
