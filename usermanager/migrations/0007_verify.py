# Generated by Django 5.0.1 on 2024-02-07 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0006_user_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.BigIntegerField()),
                ('email', models.CharField()),
                ('code', models.CharField()),
            ],
        ),
    ]
