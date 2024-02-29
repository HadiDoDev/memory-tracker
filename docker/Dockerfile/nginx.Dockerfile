# Base Image
FROM nginx:1.19.3
LABEL maintainer="HadiDo <dodangeh.hadi@gmail.com>"

# Get the dynamic values from .env file.
ARG DOMAIN_NAMES
ARG PROJECT_NAME

# Copy the file project.conf to the container.
COPY docker/Dockerfile/nginx/project.conf /etc/nginx/conf.d/

# Replace the ${} placeholders with the environment variable values.
RUN sed -i 's/{{PROJECT_NAME}}/'"${PROJECT_NAME}"'/' /etc/nginx/conf.d/project.conf
RUN sed -i 's/{{DOMAIN_NAMES}}/'"${DOMAIN_NAMES}"'/' /etc/nginx/conf.d/project.conf

EXPOSE 80
