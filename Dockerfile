FROM python:3.12-alpine

WORKDIR /app

RUN pip install poetry --no-cache-dir
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

COPY . .

COPY entrypoint.sh ./

RUN chmod +x ./entrypoint.sh

CMD ["./entrypoint.sh"]
