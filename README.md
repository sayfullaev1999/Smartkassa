# Smartkassa

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Django](https://img.shields.io/badge/django-5.1.7-green)
![Docker](https://img.shields.io/badge/Docker-Supported-blue)

## 🛠 Установка и запуск

### 🔹 Через Docker
1. **Склонируйте репозиторий:**
   ```sh
   git clone https://github.com/sayfullaev1999/Smartkassa.git
   cd Smartkassa
   ```
2. **Создайте файл `.env` на основе примера:**
   ```sh
   cp .env.example .env
   ```
   Отредактируйте `.env` файл при необходимости.
3. **Соберите и запустите контейнеры:**
   ```sh
   docker-compose up --build
   ```
4. **Откройте приложение в браузере:**
   Перейдите по адресу `http://localhost:8000`.

### 🔹 Локально (без Docker)
1. **Склонируйте репозиторий:**
   ```sh
   git clone https://github.com/sayfullaev1999/Smartkassa.git
   cd Smartkassa
   ```
2. **Создайте и активируйте виртуальное окружение:**
   ```sh
   python -m venv env
   source env/bin/activate  # Для Windows: env\Scripts\activate
   ```
3. **Установите зависимости:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Создайте файл `.env` на основе примера:**
   ```sh
   cp .env.example .env
   ```
   Отредактируйте `.env` файл при необходимости.
5. **Выполните миграции:**
   ```sh
   python src/manage.py migrate
   ```
6. **Запустите сервер разработки:**
   ```sh
   python src/manage.py runserver
   ```
7. **Откройте приложение в браузере:**
   Перейдите по адресу `http://localhost:8000`.

