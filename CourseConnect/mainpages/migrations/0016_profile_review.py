# Generated by Django 5.0.2 on 2024-03-20 22:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpages', '0015_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='review',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainpages.review'),
        ),
    ]