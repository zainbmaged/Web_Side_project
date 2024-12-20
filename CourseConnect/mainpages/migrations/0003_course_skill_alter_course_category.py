# Generated by Django 5.0.2 on 2024-03-17 00:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpages', '0002_remove_course_skill_alter_course_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='Skill',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mainpages.skill'),
        ),
        migrations.AlterField(
            model_name='course',
            name='Category',
            field=models.CharField(max_length=100),
        ),
    ]
