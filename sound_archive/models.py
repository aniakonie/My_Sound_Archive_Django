from django.db import models

class Genres(models.Model):
    genre = models.CharField(max_length=30, unique=True)
    subgenre = models.CharField(max_length=30)
