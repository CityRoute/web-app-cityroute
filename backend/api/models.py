from django.db import models
from rest_framework import serializers
from django.core.mail import send_mail  
from django_rest_passwordreset.signals import reset_password_token_created
from django.urls import reverse
from django.dispatch import receiver
import os
from django.core import mail
from django.template.loader import render_to_string
from django.utils.timezone import make_aware, now
from postgres_copy import CopyManager



class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('url', 'subject', 'body', 'pk')

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="CityRoute.ml"),
        # message:
        email_plaintext_message,
        # from:
        os.getenv("EMAIL_HOST_USER"),
        # to:
        [reset_password_token.user.email],
        # html message
        html_message=render_to_string('password_reset.html', {'reset_token': reset_password_token.key})
    )

class Weather(models.Model):
    day_number = models.IntegerField(default=1)
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
    scraped_on = models.DateTimeField(default=now, primary_key=True)

    

    def __str__(self):
        return str(self.datetime)
    class Meta:
        ordering = ['datetime']
        db_table = 'weather'
    class Admin:
        pass


class Stop(models.Model):
    name = models.CharField(default='Missing', max_length=50)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    unique_id = models.CharField(default='Missing', max_length=15)

    def __str__(self):
        return str(self.name)
    class Meta:
        db_table = 'stops'
    class Admin:
        pass
    