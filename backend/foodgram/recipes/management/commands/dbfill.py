import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredients


class Command(BaseCommand):
    def dbfill(self):
        ingredients = os.path.join(settings.BASE_DIR,
                                   'data', 'ingredients.csv')
        with open(ingredients, encoding='utf-8') as file:
            counter = 0
            for row in csv.reader(file):
                print(f'Добавлен ингредиент {row[0]}')
                Ingredients.objects.create(name=row[0],
                                           measurement_unit=row[1])
                counter += 1
            print(f'Успешно добавлено - {counter} ингредиентов.')

    def handle(self, *args, **options):
        command = input('Очистить базу перед пополнением? [y/n]')
        if command == 'y':
            Ingredients.objects.all().delete()
            print('Модель Ingredient очищена.')
            self.dbfill()
        elif command == 'n':
            self.dbfill()
        else:
            print('Неправильный ввод')
