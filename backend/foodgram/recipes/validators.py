from django.core.validators import RegexValidator


class ValidateName(RegexValidator):
    regex = '^[a-zA-Z0-9а-яА-Я]*$'
    message = 'Допустимы только цифры и буквы в названий'


class ValidateRecipeName(RegexValidator):
    regex = '^[a-zA-Z0-9а-яА-Я _]*$'
    message = 'Допустимы только цифры и буквы в названий'


class ValidateHex(RegexValidator):
    regex = '^#([A-Fa-f0-9]{3,6})$'
    message = 'Недопустимый hex код'
