# Generated by Django 3.2.4 on 2021-06-28 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_weather'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weather',
            name='created_date',
            field=models.DateTimeField(default='2021-06-28'),
        ),
    ]
