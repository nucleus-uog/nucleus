FROM python:3.6-alpine
MAINTAINER Devine Industries

# === Expected environment variables: ===
# Set these to the username and password
# that has access to the GitLab
# registries.
# NUCLEUS_REGISTRY_USERNAME changeme
# NUCLEUS_REGISTRY_PASSWORD changeme
#
# Update this to match the host container
# for docker-in-docker and add a volume
# if required.
# DOCKER_HOST /var/www/docker.sock
#
# Set the secret key.
# NUCLEUS_SECRET_KEY changeme
#
# Set the PostgreSQL connection settings.
# NUCLEUS_DB_USERNAME root
# NUCLEUS_DB_PASSWORD changeme
# NUCLEUS_DB_HOST localhost
# NUCLEUS_DB_PORT 5432
#
# Set the Redis connection settings.
# NUCLEUS_REDIS_HOST localhost
# NUCLEUS_REDIS_PORT 6379

# Use the production settings.
ENV DJANGO_SETTINGS_MODULE nucleus.production_settings

# Create working directory.
RUN mkdir /nucleus
WORKDIR /nucleus
ADD . /nucleus/

RUN apk update
# Install dependencies for building pip packages.
RUN apk add libffi libffi-dev build-base
# Install dependencies for Pillow.
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
# Install dependencies for psycopg2
RUN apk add postgresql-dev linux-headers
# Install dependencies for some npm packages.
RUN apk add automake autoconf file bash nasm pkgconfig libtool
# Install nodejs for Gulp and Docker for test runner.
RUN apk add docker nodejs

# Install gulp
RUN npm install -g gulp-cli

# Install node dependencies
RUN npm install

# Install python dependencies
RUN pip install -r requirements.txt

# Run gulp build
RUN gulp build:favicon
RUN gulp build
