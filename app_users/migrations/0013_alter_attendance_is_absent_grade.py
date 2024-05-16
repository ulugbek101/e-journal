# Generated by Django 5.0.2 on 2024-04-26 01:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0012_attendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='is_absent',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')], max_length=1, null=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_users.lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_users.student')),
            ],
        ),
    ]
