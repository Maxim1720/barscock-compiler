FROM python:3.12-slim as builder
RUN pip install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
WORKDIR /backend
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry config virtualenvs.in-project true && poetry install --no-root --only main
RUN .venv/bin/pip show uvicorn


FROM python:3.12-slim as deploy
COPY --from=builder /backend/.venv /backend/.venv
ENV PATH="/backend/.venv/bin:$PATH"
WORKDIR /backend
COPY ./src /backend/src
COPY ./entrypoint.sh .
COPY ./res/ ./res/

ENV RES_DIR=/backend/res
ENV OUT_DIR=/backend/out

RUN chmod +x entrypoint.sh
ENTRYPOINT ["bash", "entrypoint.sh"]
