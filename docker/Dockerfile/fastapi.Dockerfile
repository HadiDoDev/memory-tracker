# Base Image
FROM python:3.10-slim-buster
LABEL maintainer="Hadi Do <dodangeh.hadi@gmail.com>"

# Set default environment variables
ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set required environment variables
ARG PROJECT_ROOT
ARG PROJECT_NAME
ARG DOMAIN_NAMES
ARG DEBUG
ARG PRODUCTION_MODE

ENV PROJECT_ROOT ${PROJECT_ROOT}
ENV PROJECT_NAME ${PROJECT_NAME}
ENV DOMAIN_NAMES ${DOMAIN_NAMES}
ENV DEBUG ${DEBUG}
ENV PRODUCTION_MODE ${PRODUCTION_MODE}


RUN apt-get update -qy \
    && apt-get install apt-utils locales locales-all -y

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

ENV TZ=Asia/Tehran
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

# Update the docker container and install system dependencies
# The package python-magic requires libmagic1 to build.
# uWSGI rquires gcc to build.
RUN apt-get upgrade -qy \
    && apt-get install sudo nano cron -y \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Create and set a working directory in the container
WORKDIR ${PROJECT_ROOT}

# Install the required packages for our project
COPY app/poetry.lock .
COPY app/pyproject.toml .

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Copy project files to the working directory
COPY app .

# Create a user by the name of "user" and set "user" password.
RUN adduser user --disabled-login --disabled-password && echo "user:user" | chpasswd && adduser user sudo

# Change permission of media folder
RUN chown -R user:user /srv/
RUN chmod -R 755 /srv/

# Switch to the non-root user.
USER user

# Finally run the project
ENTRYPOINT ["/bin/bash", "-c", "${PROJECT_ROOT}/entrypoint.sh"]
EXPOSE 8000