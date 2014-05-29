from django.db import models

# Create your models here.

class Musician(models.Model):

    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    instrument = models.CharField(max_length=100)

class Album(models.Model):

    musician = models.ForeignKey(Musician)
    title = models.CharField(max_length=100)
    release_date = models.DateTimeField(auto_now_add=True)
    num_stars = models.IntegerField()