# Generated by Django 3.2.6 on 2021-08-10 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210808_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='routeid',
            field=models.CharField(default='Missing',
                                   max_length=20,
                                   primary_key=True,
                                   serialize=False),
        ),
    ]