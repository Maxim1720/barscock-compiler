FROM debian:stable as build
RUN apt update
RUN apt install python3 nasm pip pipx -y
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN export PATH="$HOME/.poetry/bin:$PATH"

#FROM build as prod

COPY . backend
WORKDIR /backend
ENTRYPOINT ["python3", "src/analyzer_v2/main.py"]