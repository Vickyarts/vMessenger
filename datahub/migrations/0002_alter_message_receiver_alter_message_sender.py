# Generated by Django 5.0.1 on 2024-02-08 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datahub', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='receiver',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.BigIntegerField(),
        ),
    ]
