# Generated by Django 4.2.7 on 2023-11-29 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_course_is_listed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='is_listed',
            field=models.BooleanField(default=False),
        ),
    ]
