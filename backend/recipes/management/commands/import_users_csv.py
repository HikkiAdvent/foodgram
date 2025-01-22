from django.contrib.auth import get_user_model

from .base_import_command import BaseImportCommand

User = get_user_model()


class Command(BaseImportCommand):
    help = 'Импорт пользователей из CSV файла'

    def import_data(self, reader):
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
