# Generated by Django 5.0.2 on 2024-04-28 18:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0017_alter_useraccount_parent_of'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='parent_of',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parent_students', to='app_users.parent'),
        ),
    ]