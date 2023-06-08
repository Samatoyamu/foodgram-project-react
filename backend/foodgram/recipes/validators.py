import re

from django.core.exceptions import ValidationError


def validate_name(value):
    reg = re.compile(r'^[a-zA-Z0-9а-яА-Я]*$')
    if not reg.match(value):
        raise ValidationError('Допустимы только цифры и буквы в названий')


def validate_hex(value):
    reg = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    if not reg.match(value):
        raise ValidationError('Недопустимый hex код')
