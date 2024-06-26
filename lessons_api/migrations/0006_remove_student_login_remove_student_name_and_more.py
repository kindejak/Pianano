# Generated by Django 4.2.9 on 2024-03-13 21:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lessons_api', '0005_alter_question_question_json'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='login',
        ),
        migrations.RemoveField(
            model_name='student',
            name='name',
        ),
        migrations.RemoveField(
            model_name='student',
            name='nickname',
        ),
        migrations.RemoveField(
            model_name='student',
            name='password_hash',
        ),
        migrations.RemoveField(
            model_name='student',
            name='surname',
        ),
        migrations.AddField(
            model_name='student',
            name='streak',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('NI', 'Note idetification'), ('CI', 'Chord idetification'), ('PN', 'Play note'), ('PC', 'Play chord')], max_length=2),
        ),
    ]
