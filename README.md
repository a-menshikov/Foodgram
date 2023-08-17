# Проект "Продуктовый помощник"

Если вам помог этот репозиторий - не пожалейте звездочки для него))

## Описание проекта

Приложение «Продуктовый помощник» - это сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

## Техническая информация

Стек технологий: Python 3, Django, DjangoRestFramework, Docker, Docker Compose, Nginx, Postgres, React

Веб-сервер: nginx
Frontend фреймворк: React
Backend фреймворк: Django
API фреймворк: Django REST
База данных: PostgreSQL

Веб-сервер nginx перенаправляет запросы клиентов к контейнерам frontend и backend, либо к хранилищам (volume) статики и файлов.
Контейнер nginx взаимодействует с контейнером backend через gunicorn.
Контейнер frontend взаимодействует с контейнером backend посредством API-запросов.

## Документация к проекту

Документация для API после установки доступна по адресу

```url
    /api/docs/redoc.html
```

## Запуск проекта через Docker

1. Клонировать репозиторий и перейти в него в командной строке:
Для развертывания на моих образах потребуются только файлы docker-compose.yml и nginx.conf.
Для сборки своих образов с доработанным кодом - откорректируйте файл docker-compose.yml чтобы образы билдились, а не скачивались.

    ```bash
    git clone <ссылка с git-hub>
    ```

2. Шаблон наполнения .env (не включен в текущий репозиторий), расположить по пути infra/.env

    ```text
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME= # имя базы данных
    POSTGRES_USER= # логин для подключения к базе данных
    POSTGRES_PASSWORD= # пароль для подключения к БД (установите свой)
    DB_HOST=database
    DB_PORT= # порт для подключения к БД
    SECRET_KEY= # секретный ключ Django
    DEBUG= # True или False
    ALLOWED_HOSTS= # через запятую
    ```

    также настройте адрес сервера в nginx.conf.

3. Находясь в папке infra/ поднять контейнеры

    ```bash
    docker-compose up -d --build
    ```

4. Выполнить миграции:

    ```bash
    docker-compose exec backend python manage.py migrate
    ```

5. Создать суперпользователя:

    ```bash
    docker-compose exec backend python manage.py createsuperuser
    ```

6. Собрать статику:

    ```bash
    docker-compose exec backend python manage.py collectstatic --no-input
    ```

7. Наполнить базу заранее заготовленными файлами:

    ```bash
    docker-compose exec backend python manage.py import_data
    ```
