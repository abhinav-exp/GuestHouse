# Generated by Django 3.1.7 on 2021-02-27 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Organiser', '0008_auto_20210227_1149'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guest',
            old_name='Come_to',
            new_name='Attending',
        ),
    ]
