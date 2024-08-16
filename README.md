# Django websocket emails loader

Небольшой сервис для получения писем из почтового ящика пользователя по протоколу прикладного уровня imap в режиме реального времени с сохранением в БД и отображением статуса загрузки в прогрэсбаре.

# Стек
* Python 3.12
* Django 4.2
* bootstrap5
* Django channels 4.1.0
* Docker
* PostgreSQL
* imaplib
* HTML5
* CSS
* JS

# Установка и запуск
В корне проекта создайте файл и наполните его по аналогии с `.env.example`:
```
POSTGRES_USER=ваш пользователь
POSTGRES_PASSWORD=ваш пароль
POSTGRES_DB=ваше название БД
DB_HOST=db
DB_PORT=5432
```

Из корневой дирректории выполните
```sh
docker compose up
```

ВСË!

Установка и запуск в режиме разработки:
* замените значение переменной DB_HOST в `.env` на `localhost`

```sh
pip install poetry
```

```sh
poetry install
```

* Примените миграции:

```sh
python manage.py migrate
```

* Запустите сервер разработки:

```sh
python manage.py runserver
```

# Использование
Заполните поля формы:
* укажите вашу почту на gmail, yandex или mail.ru
* укажите полученный пароль-приложений от imap-сервера
* укажите провайдера
* если ничего не упало - НАСЛАЖДАЙТЕСЬ!