# Generated by Django 2.2 on 2019-05-06 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0004_movie_imdb_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.DecimalField(decimal_places=2, max_digits=2),
        ),
    ]
