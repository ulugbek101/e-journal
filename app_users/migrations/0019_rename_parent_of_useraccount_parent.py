# Generated by Django 5.0.2 on 2024-04-28 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0018_alter_useraccount_parent_of'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraccount',
            old_name='parent_of',
            new_name='parent',
        ),
    ]
