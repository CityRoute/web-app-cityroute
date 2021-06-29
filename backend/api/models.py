from django.db import models
from rest_framework import serializers
from django.utils.timezone import now



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
    temp_day = models.FloatField(default=0)
    temp_min = models.FloatField(default=0)
    temp_max = models.FloatField(default=0)
    temp_night = models.FloatField(default=0)
    temp_eve = models.FloatField(default=0)
    temp_morn = models.FloatField(default=0)
    datetime = models.DateTimeField(default=now, editable=False)
    temperature = models.FloatField(default=0)
    windDirection = models.FloatField(default=0)
    windSpeed = models.FloatField(default=0)
    humidity = models.FloatField(default=0)
    pressure = models.FloatField(default=0)
    clouds = models.FloatField(default=0)
    precipitation = models.FloatField(default=0)
    weatherid = models.IntegerField(default=0)
    # created_date = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return str(self.datetime)
    class Meta:
        ordering = ['datetime']
    class Admin:
        pass