# Generated by Django 4.2.7 on 2023-12-18 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("lessons_api", "0004_alter_question_question_json")]

    operations = [
        migrations.AlterField(
            model_name="question", name="question_json", field=models.TextField()
        )
    ]
