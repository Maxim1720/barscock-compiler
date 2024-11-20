FROM nginx:1.25.0-alpine
COPY ./frontend/ /usr/share/nginx/html/

WORKDIR /etc/nginx/
COPY ./nginx/nginx.conf .
COPY ./nginx/templates/ ./templates/

RUN echo "" > /etc/nginx/conf.d/default.conf

# ENTRYPOINT [ "nginx", "-g", "daemon off;" ]