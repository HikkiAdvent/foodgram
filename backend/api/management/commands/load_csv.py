import csv
import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Import data from CSV files to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-dir',
            type=str,
            default=str(Path(settings.BASE_DIR, 'static', 'data')),
            help='Path to the directory with CSV files',
        )
        parser.add_argument(
            '--files',
            type=str,
            nargs='+',
            help=(
                'List of files to import in the format:'
                ' file:model[:field_mapping]'
            )
        )

    def handle(self, *args, **options):
        csv_file_path = options['csv_dir']
        file_path = os.path.join(csv_file_path, 'ingredients.csv')
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if len(row) == 2:
                    name, unit = row
                    Ingredient.objects.update_or_create(name=name, measurement_unit=unit)

        self.stdout.write(self.style.SUCCESS('Ingredients loaded successfully'))
