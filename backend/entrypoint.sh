#!/bin/bash
# Убедитесь, что переменные окружения корректно передаются

exec uvicorn src.main:app --reload --host=${HOST} --port=${BACKEND_PORT}