# Generated by Django 4.2.7 on 2023-12-15 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.TextField(),
        ),
    ]
