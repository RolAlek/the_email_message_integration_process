FROM python:3.12-alpine

WORKDIR /app

RUN pip install poetry --no-cache-dir
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

COPY the_message_integration_project/ .

CMD ["python", "the_message_integration_project/manage.py", "runserver", "0.0.0.0:8000"]
