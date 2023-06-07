import re

from django.core.exceptions import ValidationError


def validate_regex(value):
    reg = re.compile(r'^[a-zA-Z0-9а-яА-Я]*$')
    if not reg.match(value):
        raise ValidationError('Допустимы только цифры и буквы в названий')
