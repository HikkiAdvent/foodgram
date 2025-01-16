Находясь в папке infra, выполните команду docker-compose up. При выполнении этой команды контейнер frontend, описанный в docker-compose.yml, подготовит файлы, необходимые для работы фронтенд-приложения, а затем прекратит свою работу.

По адресу http://localhost изучите фронтенд веб-приложения, а по адресу http://localhost/api/docs/ — спецификацию API.

python manage.py load_csv --csv-dir=/home/valerij/dev/foodgram/data --files=ingredients.csv:Ingredient
# Загрузка ингредиентов
python manage.py import_csv_db /home/valerij/dev/foodgram/data/ingredients.csv

          sudo docker compose -f docker-compose.production.yml exec backend python manage.py import_csv_db
          sudo docker compose -f docker-compose.production.yml exec backend python manage.py import_tags_csv_db