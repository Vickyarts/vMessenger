# Generated by Django 5.0.1 on 2024-02-07 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0003_rename_first_name_user_display_remove_user_last_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='created_at',
            new_name='joined_at',
        ),
    ]