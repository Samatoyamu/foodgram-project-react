from django.core.validators import RegexValidator


class validate_name(RegexValidator):
    regex = '^[a-zA-Z0-9а-яА-Я]*$'
    message = 'Допустимы только цифры и буквы в названий'


class validate_hex(RegexValidator):
    regex = '^#([A-Fa-f0-9]{3,6})$'
    message = 'Недопустимый hex код'
