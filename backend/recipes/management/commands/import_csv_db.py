from recipes.models import Ingredient
from .base_import_command import BaseImportCommand


class Command(BaseImportCommand):
    help = 'Импорт ингредиентов из CSV файла'

    def import_data(self, reader):
        for row in reader:
            name = row['name']
            measurement_unit = row['measurement_unit']
            ingredient, created = Ingredient.objects.get_or_create(
                name=name,
                measurement_unit=measurement_unit
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Ингредиент "{name}" успешно добавлен.'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Ингредиент "{name}" уже существует.'
                    )
                )
