from django.db import models
from rest_framework import serializers
from django.utils.timezone import make_aware, now


class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('url', 'subject', 'body', 'pk')


class Weather(models.Model):
    # lon = models.FloatField()
    # lat = models.FloatField()
    day_number = models.IntegerField(default=1, primary_key=True)
    temp_day = models.FloatField(default=0)
    temp_min = models.FloatField(default=0)
    temp_max = models.FloatField(default=0)
    temp_night = models.FloatField(default=0)
    temp_eve = models.FloatField(default=0)
    temp_morn = models.FloatField(default=0)
    datetime = models.DateTimeField(default=now)
    windDirection = models.FloatField(default=0)
    windSpeed = models.FloatField(default=0)
    humidity = models.FloatField(default=0)
    pressure = models.FloatField(default=0)
    clouds = models.FloatField(default=0)
    precipitation = models.FloatField(default=0)
    weatherid = models.IntegerField(default=0)
    scraped_on = models.DateTimeField(default=now)

    

    def __str__(self):
        return str(self.datetime)
    class Meta:
        ordering = ['datetime']
        db_table = 'weather'
        unique_together = ['day_number', 'scraped_on']
    class Admin:
        pass