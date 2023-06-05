import re

from django.core.exceptions import ValidationError


def validate_regex(value):
    reg = re.compile(r'^[-a-zA-Z0-9_]+')
    if not reg.match(value):
        raise ValidationError('Имя не соответствует регулярному выражению')
