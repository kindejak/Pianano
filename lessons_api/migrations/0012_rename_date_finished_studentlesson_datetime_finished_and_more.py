# Generated by Django 4.2.9 on 2024-05-28 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons_api', '0011_alter_musiclesson_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentlesson',
            old_name='date_finished',
            new_name='datetime_finished',
        ),
        migrations.RemoveField(
            model_name='studentlesson',
            name='time_finished',
        ),
    ]
