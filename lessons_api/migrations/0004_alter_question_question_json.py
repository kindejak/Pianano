# Generated by Django 4.2.7 on 2023-11-06 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lessons_api", "0003_student_login_student_password_hash_pianoclass_and_more")
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="question_json",
            field=models.CharField(max_length=1000),
        )
    ]
