FROM python:3.6-alpine
MAINTAINER Devine Industries

# Check the nucleus.env.example file for what
# environment variables this container expects.

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
RUN apk add mariadb-dev linux-headers
# Install dependencies for some npm packages.
RUN apk add automake autoconf file bash nasm pkgconfig libtool tar bzip2
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
RUN python3 manage.py collectstatic --noinput

# Use the production settings.
ENV DJANGO_SETTINGS_MODULE nucleus.production_settings
