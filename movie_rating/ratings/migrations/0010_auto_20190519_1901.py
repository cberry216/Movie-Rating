# Generated by Django 2.2 on 2019-05-19 19:01

from django.db import migrations, models
import ratings.models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0009_auto_20190519_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.FloatField(validators=[ratings.models.validate_rating]),
        ),
    ]
