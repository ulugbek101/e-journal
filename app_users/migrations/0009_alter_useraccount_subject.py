# Generated by Django 4.2.10 on 2024-04-12 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0001_initial'),
        ('app_users', '0008_alter_lesson_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app_main.subject'),
        ),
    ]
