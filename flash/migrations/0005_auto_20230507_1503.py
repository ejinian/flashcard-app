# Generated by Django 3.1.4 on 2023-05-07 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flash', '0004_auto_20230507_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcard',
            name='current_bin',
            field=models.CharField(default='0', max_length=200),
        ),
    ]
