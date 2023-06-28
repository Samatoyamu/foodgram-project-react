# Дипломный проект "Продуктовый помощник"
Проект выполнил студент 51 когорты Яндекс Практикума  
Петушков Роман

### Описание

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Запуск проекта
Проект выполнен полностью в докер контейнерах

В директорий infra создайте файл .env и заполните следующим образом:

```
SECRET_KEY='django-insecure-_!1qxr_gpq=kf03w-g6eo(_9*p+)ex*qt1ug59h9bqjvr!2qp2'
ALLOWED_HOSTS='*'
DEBUG=True
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

- в папке infra выполняем:

```
docker-compose up -d
```

Выполняем миграций:

```
sudo docker container exec -it foodgram-backend-1 python manage.py migrate
```

Собираем статику:

```
sudo docker container exec -it foodgram-backend-1 python manage.py collectstatic --no-input
```
