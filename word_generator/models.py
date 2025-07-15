from django.db import models

class Words_db(models.Model):

    german_word=models.CharField(max_length=35)
    polish_translation=models.CharField(max_length=35)
# Create your models here.

    def __str__(self):
        return self.german_word  # 👈 This controls what shows when printed
