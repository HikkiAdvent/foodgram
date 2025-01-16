import os
import csv

from django.core.files import File
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
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
                image_path = os.path.join(
                    'foodgram_backend/data/',
                    row['image']
                )
                recipes = Recipe.objects.filter(
                    author=author,
                    name=row['name']
                )
                if recipes.exists():
                    recipe = recipes.first()
                    self.stdout.write(
                        self.style.WARNING(
                            f'Рецепт "{recipe.name}" уже существует.'
                        )
                    )
                else:
                    recipe = Recipe(
                        author=author,
                        name=row['name'],
                        text=row['text'],
                        cooking_time=row['cooking_time']
                    )
                    with open(image_path, 'rb') as image_file:
                        recipe.image.save(
                            os.path.basename(image_path),
                            File(image_file),
                            save=False
                        )
                    recipe.save()
                    recipe.ingredients.add(*ingredients)
                    recipe.tags.add(*tags)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Рецепт "{recipe.name}" успешно добавлен.'
                        )
                    )
