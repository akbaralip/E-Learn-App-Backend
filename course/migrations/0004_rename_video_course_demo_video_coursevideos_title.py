# Generated by Django 4.2.7 on 2023-11-23 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_coursevideos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='video',
            new_name='demo_video',
        ),
        migrations.AddField(
            model_name='coursevideos',
            name='title',
            field=models.CharField(default='Default Title', max_length=255),
        ),
    ]
