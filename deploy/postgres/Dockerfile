FROM postgres:16

RUN apt-get update && apt-get install -y gettext-base

COPY postgresql.conf /etc/postgresql/postgresql.conf
COPY pg_hba.conf /etc/postgresql/pg_hba.conf
COPY initial.sql /tmp/initial.sql
RUN mkdir -p "/var/log/postgresql/"

ARG POSTGRES_USER
ARG POSTGRES_DB
ARG POSTGRES_PASSWORD
RUN POSTGRES_USER=${POSTGRES_USER} POSTGRES_DB=${POSTGRES_DB} POSTGRES_PASSWORD=${POSTGRES_PASSWORD} envsubst < /tmp/initial.sql > /docker-entrypoint-initdb.d/initial.sql

EXPOSE 5432

CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf", "-c", "hba_file=/etc/postgresql/pg_hba.conf"]