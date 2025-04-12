FROM python:3.12.2-slim


# Установка системних залежностей
RUN apt-get update && apt-get install -y curl build-essential

# Встановлюємо poetry
ENV POETRY_VERSION=1.7.1

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Робоча директорія
WORKDIR /app

# Копіюємо файли
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

# Потім копіюємо увесь проект
COPY . .

# Відкриваємо порт
EXPOSE 8000

# Запускаємо сервер
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
