# Generated by Django 4.2.9 on 2024-04-15 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons_api', '0009_studentlesson_time_finished'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('NI', 'Note idetification'), ('CI', 'Chord idetification'), ('PN', 'Play note'), ('PC', 'Play chord'), ('NA', 'Note audioidetification'), ('CA', 'Chord audioidetification')], max_length=2),
        ),
    ]
