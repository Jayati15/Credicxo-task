# Generated by Django 3.2.11 on 2022-02-26 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schoolmanageapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraccount',
            old_name='User',
            new_name='user',
        ),
    ]
