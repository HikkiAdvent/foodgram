import csv

from django.core.management.base import BaseCommand


class BaseImportCommand(BaseCommand):
    help = 'Импорт данных из CSV файла'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv_file',
            type=str,
            default='data/default.csv',
            help='Путь к CSV файлу'
        )

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            self.import_data(reader)

    def import_data(self, reader):
        """Метод для переопределения."""

        raise NotImplementedError(
            'Метод import_data должен быть реализован в подклассе'
        )
