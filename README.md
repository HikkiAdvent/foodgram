# Foodgram Project

## Описание
Foodgram — это платформа для обмена рецептами. Пользователи могут:
- Выкладывать свои рецепты.
- Просматривать рецепты других пользователей.
- Подписываться на других пользователей.
- Добавлять рецепты в избранное.
- Формировать список покупок из выбранных рецептов.
- Скачивать список покупок.

## Технологии
Проект использует следующие технологии:
- **Python(Django)** — серверная логика приложения.
- **Docker** — контейнеризация сервисов.
- **PostgreSQL** — база данных.
- **React** — клиентская часть приложения.
- **Nginx** — прокси-сервер для маршрутизации запросов.

## Установка
Для развёртывания проекта выполните следующие шаги:

1. Скачайте и запустите Docker-контейнеры:
   ```bash
   sudo docker compose -f docker-compose.production.yml pull
   sudo docker compose -f docker-compose.production.yml up -d
   ```

2. Примените миграции базы данных:
   ```bash
   sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
   ```

3. Соберите статику проекта:
   ```bash
   sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic --noinput
   ```

## Опционально: добавление данных на сервер
Для импорта данных в базу выполните следующие команды:

- Импортингредиентов:
  ```bash
  sudo docker compose -f docker-compose.production.yml exec backend python manage.py import_csv_db
  ```

- Импорт тегов:
  ```bash
  sudo docker compose -f docker-compose.production.yml exec backend python manage.py import_tags_csv_db
  ```

- Импорт пользователей:
  ```bash
  sudo docker compose -f docker-compose.production.yml exec backend python manage.py import_users_csv
  ```

- Импорт рецептов:
  ```bash
  sudo docker compose -f docker-compose.production.yml exec backend python manage.py import_recipes_csv
  ```

## Автор
HikkiAdvent

