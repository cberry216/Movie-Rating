# Generated by Django 2.2 on 2019-04-16 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GroupAdmin',
            new_name='GroupAdminMember',
        ),
    ]
