from django.core.management.base import BaseCommand
from travelInfo.models import District
import requests

class Command(BaseCommand):

    help = 'Seed districts data into the database from a JSON file'

    def handle(self, *args, **kwargs):

        url = 'https://raw.githubusercontent.com/strativ-dev/technical-screening-test/main/bd-districts.json'

        response = requests.get(url)
        data = response.json()

        District.objects.all().delete()

        for district_data in data['districts']:
            District.objects.create(**district_data)

        self.stdout.write(self.style.SUCCESS('Data seeded successfully'))
