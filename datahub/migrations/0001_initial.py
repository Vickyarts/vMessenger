# Generated by Django 5.0.1 on 2024-02-07 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.IntegerField()),
                ('receiver', models.IntegerField()),
                ('text', models.TextField()),
                ('created_at', models.DateField()),
                ('received_at', models.DateField()),
            ],
        ),
    ]