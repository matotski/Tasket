# Tasket

## Описание
Этот проект представляет собой систему управления задачами, которая позволяет пользователям управлять проектами, задачами и комментариями. Пользователи могут быть назначены на роли в рамках проектов и получать уведомления по электронной почте при добавлении в проект.
## Функции
- Регистрация пользователей и аутентификация
- Управление проектами
- Управление задачами
- Назначение ролей в рамках проектов
- Комментирование задач
- Уведомления по электронной почте

## Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   
2. Создайте виртуальное окружение и активируйте его:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # Для Linux/MacOS используйте source venv/bin/activate

3. Установите необходимые пакеты:
    ```bash
    pip install -r requirements.txt
   
4. Примените миграции:
    ```bash
    python manage.py migrate

5. Запустите сервер разработки:
    ```bash
    python manage.py runserver

## Использование
Доступ к приложению по адресу http://127.0.0.1:8000/. Используйте API-эндпоинты для управления пользователями, проектами, задачами и комментариями.

# Инструкция по развертыванию

## Требования

Перед началом убедитесь, что у вас установлены следующие компоненты:
- Docker (версия 20.10 или выше)
- Docker Compose (если вы используете Docker Compose)

## Шаги по развертыванию
1. Клонируйте репозиторий
   ```bash
   git clone https://github.com/matotski/Tasket.git
   cd Tasket
2. Убедитесь, что у вас есть файл Dockerfile с содержимым:
   ```bash
   FROM python:3.13

   ENV PYTHONDONTWRITEBYTECODE=1
   ENV PYTHONUNBUFFERED=1

   WORKDIR /app

   COPY requirements.txt .

   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   RUN python manage.py migrate

   EXPOSE 8000

   CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
3. Убедитесь, что у вас есть файл docker-compose.yml с содержимым:
   ```bash
   version: '3.13'

   services:
   web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - PYTHONDONTWRITEBYTECODE=1
      - PYTHONUNBUFFERED=1
    command: python manage.py runserver 0.0.0.0:8000

   volumes:
   db_data:
4. Запустите контейнер с помощью Docker Compose:
   ```bash
   docker-compose up --build
Теперь вы можете получить доступ к вашему приложению в браузере по адресу:
http://localhost:8000