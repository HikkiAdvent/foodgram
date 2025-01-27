from django.core.exceptions import ValidationError


def me_validator(value):
    if value.lower() == 'me':
        raise ValidationError(
            f'Никнейм не может быть {value} ',
        )
