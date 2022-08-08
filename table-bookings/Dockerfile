FROM python:3.9
ENV PYTHONUNBUFFERED 1

ENV PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.1.12 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

COPY .env /

WORKDIR /app
COPY table_bookings/. /app/
COPY poetry.lock pyproject.toml /app/
RUN pip install poetry
RUN poetry install


EXPOSE 8000
CMD ["poetry", "shell"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]