# Generated by Django 3.2.4 on 2021-06-28 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_weather_created_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weather',
            name='created_date',
        ),
    ]
