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
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args,
                                 **kwargs):

    email_plaintext_message = "{}?token={}".format(
        reverse('password_reset:reset-password-request'),
        reset_password_token.key)

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
        html_message=render_to_string(
            'password_reset.html', {'reset_token': reset_password_token.key}))


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
    rain = models.FloatField(default=0.0)
    main = models.CharField(default="Missing", max_length=20)
    description = models.CharField(default="Missing", max_length=50)
    scraped_on = models.DateTimeField(default=now, primary_key=True)

    def __str__(self):
        return str(self.datetime)

    class Meta:
        ordering = ['datetime']
        db_table = 'weather'

    class Admin:
        pass


class Stop(models.Model):
    number = models.IntegerField(default=0, unique=True)
    unique_id = models.CharField(default='Missing',
                                 max_length=15,
                                 primary_key=True)
    name = models.CharField(default='Missing', max_length=50)
    avg_dwelltime = models.FloatField(default=0)

    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    def __str__(self):
        return str(self.number)

    class Meta:
        db_table = 'stops'

    class Admin:
        pass


class FavouriteStop(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             default='Missing',
                             related_name='favstops')
    stopid = models.ForeignKey('Stop',
                               on_delete=models.CASCADE,
                               default='Missing',
                               related_name='favstops',
                               to_field='unique_id')

    def __str__(self):
        return f"{self.user}-{self.stopid}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'stopid'],
                                    name='unique_favourite')
        ]
        pass

    class Admin:
        pass


class FavouriteRoute(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             default='Missing',
                             related_name='favroutes')
    routeid = models.ForeignKey('Route',
                                on_delete=models.CASCADE,
                                default='Missing',
                                related_name='favroutes',
                                to_field='routeid')

    def __str__(self):
        return f"{self.user}-{self.routeid}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'routeid'],
                                    name='unique_favourite_route')
        ]
        pass

    class Admin:
        pass


class FavouriteDirections(models.Model):
    directions_id = models.AutoField(primary_key=True, )
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             default='Missing',
                             related_name='favdirections')
    origin = models.TextField(default='Missing', )
    destination = models.TextField(default='Missing', )
    url = models.TextField(default='Missing', )

    def __str__(self):
        return f"{self.user}-{self.origin}-{self.destination}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'directions_id'],
                                    name='unique_favourite_directions')
        ]
        pass

    class Admin:
        pass


class Route(models.Model):
    routeid = models.CharField(default='Missing',
                               primary_key=True,
                               max_length=20)

    def __str__(self):
        return self.routeid

    class Meta:
        pass

    class Admin:
        pass


class RouteStop(models.Model):
    routeid = models.ForeignKey('Route',
                                on_delete=models.CASCADE,
                                default='Missing',
                                related_name='routestops',
                                to_field='routeid')
    stopnumber = models.ForeignKey('Stop',
                                   on_delete=models.CASCADE,
                                   default='Missing',
                                   related_name='routestops',
                                   to_field='number')
    outbound_yn = models.BooleanField(default=0)
    order = models.IntegerField(default=0)
    percent_of_route = models.FloatField(default=0)

    def __str__(self):
        return f"{self.routeid}-{self.stopnumber}"

    class Meta:
        pass

    class Admin:
        pass


class Review(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             default='Missing',
                             related_name='review')
    content = models.CharField(default='Missing', max_length=350)
    clean_rating = models.IntegerField(default=0)
    speed_rating = models.IntegerField(default=0)
    accuracy_rating = models.IntegerField(default=0)
    routeid = models.ForeignKey('Route',
                                on_delete=models.CASCADE,
                                default='Missing',
                                related_name='routereview',
                                to_field='routeid')

    def __str__(self):
        return f"{self.user}-{self.content}"

    class Meta:
        app_label = 'api'

    class Admin:
        pass
