# Generated by Django 3.2.4 on 2021-06-28 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_weather_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weather',
            name='created_date',
            field=models.DateTimeField(default=1624880820.496175),
        ),
    ]
