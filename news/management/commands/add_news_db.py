import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from news.models import News

class Command(BaseCommand):
    help = 'Carga 5 noticias desde Fake.csv'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(os.path.dirname(__file__), 'Fake.csv')

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                if count >= 5:
                    break
                try:
                    date_value = datetime.strptime(row['date'], '%B %d, %Y').date()
                except ValueError:
                    continue  # se saltan filas con fecha en formato distinto

                News.objects.create(
                    headline=row['title'],
                    body=row['text'][:1000],
                    date=date_value,
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'{count} noticias cargadas.'))