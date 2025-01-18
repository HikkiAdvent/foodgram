from django.core.exceptions import ValidationError


def me_validator(value):
    if value == 'me' or value == 'Me':
        raise ValidationError(
            f'Никнейм не может быть {value} ',
        )
