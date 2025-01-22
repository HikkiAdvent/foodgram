from recipes.models import Tag
from .base_import_command import BaseImportCommand


class Command(BaseImportCommand):
    help = 'Импорт тегов из CSV файла'

    def import_data(self, reader):
        for row in reader:
            name = row['name']
            slug = row['slug']
            tag, created = Tag.objects.get_or_create(
                name=name,
                slug=slug
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Тег "{name}" успешно добавлен.'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Тег "{name}" уже существует.'
                    )
                )
