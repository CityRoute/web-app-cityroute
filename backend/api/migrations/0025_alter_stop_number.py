# Generated by Django 3.2.5 on 2021-07-14 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_stop_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stop',
            name='number',
            field=models.IntegerField(default=0),
        ),
    ]
