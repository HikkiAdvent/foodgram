import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Импорт пользователей из CSV файла'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv_file',
            type=str,
            default='foodgram_backend/data/users.csv',
            help='Путь к CSV файлу с данными пользователей'
        )

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                username = row['username']
                email = row['email']
                first_name = row['first_name']
                last_name = row['last_name']
                password = row['password']
                user, created = User.objects.get_or_create(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                if created:
                    user.set_password(password)
                    user.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Пользователь "{username}" успешно добавлен.'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Пользователь "{username}" уже существует.'
                        )
                    )
