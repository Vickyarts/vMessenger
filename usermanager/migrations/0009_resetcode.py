# Generated by Django 5.0.1 on 2024-03-18 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0008_alter_user_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResetCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.BigIntegerField()),
                ('email', models.CharField()),
                ('resetcode', models.CharField()),
                ('passcode', models.CharField()),
            ],
        ),
    ]