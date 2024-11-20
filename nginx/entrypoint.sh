#!/bin/bash

# Подставляем переменные окружения в конфиг
envsubst < /etc/nginx/templates/*.template > /etc/nginx/conf.d/


# Запускаем NGINX


cat /etc/nginx/nginx.conf