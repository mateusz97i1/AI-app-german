import json
from django.core.management.base import BaseCommand
from word_generator.models import Words_db

class Command(BaseCommand):
    help = 'Load data from a JSON file into the database'

    def handle(self, *args, **kwargs):
        # Open and load the JSON file
        with open('D:/django/german_apps/german_app/word_generator/templates/words.json', 'r') as f:
            data = json.load(f)
        
        # Iterate through the dictionary and create objects
        for german_word, polish_translation in data.items():
            Words_db.objects.create(
                german_word=german_word,
                polish_translation=polish_translation
            )
        
        # Confirm success
        self.stdout.write(self.style.SUCCESS('Successfully imported JSON data to the database.'))
