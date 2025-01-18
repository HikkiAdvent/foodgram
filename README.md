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

- **Python** — серверная логика приложения.
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

- Импорт ингредиентов:

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

### Пример API запросов

**GET** `/api/recipes/` - получение списка рецептов

```json
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Иванов",
        "is_subscribed": false,
        "avatar": "http://foodgram.example.org/media/users/image.png"
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.png",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

**POST** `/api/recipes/` - добавление рецепта

```json
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

**POST** `/api/users/` - регистрация пользователя

```json
{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Иванов",
  "password": "Qwerty123"
}
```

## Автор

HikkiAdvent

