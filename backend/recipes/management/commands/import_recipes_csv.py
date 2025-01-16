import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from recipes.models import Recipe, Ingredient, Tag

User = get_user_model()


class Command(BaseCommand):
    help = 'Импорт рецептов из CSV файла'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv_file',
            type=str,
            default='foodgram_backend/data/recipes.csv',
            help='Путь к CSV файлу'
        )

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                author = User.objects.get(username=row['author'])
                tags = Tag.objects.filter(id__in=row['tags'].split(';'))
                ingredients = Ingredient.objects.filter(
                    id__in=row['ingredients'].split(';')
                )
                image_path = row['image']
                recipe, created = Recipe.objects.get_or_create(
                    author=author,
                    name=row['name'],
                    text=row['text'],
                    cooking_time=row['cooking_time'],
                    image=image_path
                )
                if created:
                    for ingredient in ingredients:
                        recipe.ingredients.add(ingredient)
                    for tag in tags:
                        recipe.tags.add(tag)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Рецепт "{recipe.name}" успешно добавлен.'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Рецепт "{recipe.name}" уже существует.'
                        )
                    )
