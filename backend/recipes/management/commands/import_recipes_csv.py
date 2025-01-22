import os

from django.core.files import File
from django.contrib.auth import get_user_model

from recipes.models import Recipe, Ingredient, Tag
from .base_import_command import BaseImportCommand

User = get_user_model()


class Command(BaseImportCommand):
    help = 'Импорт рецептов из CSV файла'

    def import_data(self, reader):
        for row in reader:
            author = User.objects.get(username=row['author'])
            tags = Tag.objects.filter(id__in=row['tags'].split(';'))
            ingredients = Ingredient.objects.filter(
                id__in=row['ingredients'].split(';')
            )
            image_path = os.path.join('data/', row['image'])
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
