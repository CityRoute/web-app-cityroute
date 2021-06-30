from django.db import models
from rest_framework import serializers
from django.core.mail import send_mail  
from django_rest_passwordreset.signals import reset_password_token_created
from django.urls import reverse
from django.dispatch import receiver
import os
from django.core import mail

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
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        os.getenv("EMAIL_HOST_USER"),
        # to:
        [reset_password_token.user.email]
    )
