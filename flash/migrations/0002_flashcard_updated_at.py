# Generated by Django 3.1.4 on 2023-05-06 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flash', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flashcard',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]