# Generated by Django 3.2.6 on 2021-08-08 10:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_auto_20210808_1033'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteDirections',
            fields=[
                ('directions_id', models.AutoField(primary_key=True, serialize=False)),
                ('origin', models.TextField(default='Missing')),
                ('destination', models.TextField(default='Missing')),
                ('url', models.TextField(default='Missing')),
                ('user', models.ForeignKey(default='Missing', on_delete=django.db.models.deletion.CASCADE, related_name='favdirections', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='favouritedirections',
            constraint=models.UniqueConstraint(fields=('user', 'directions_id'), name='unique_favourite_directions'),
        ),
    ]
