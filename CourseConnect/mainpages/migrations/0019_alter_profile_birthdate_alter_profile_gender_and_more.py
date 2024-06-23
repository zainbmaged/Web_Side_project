# Generated by Django 5.0.2 on 2024-03-21 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpages', '0018_review_created_at_review_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='language',
            field=models.CharField(blank=True, choices=[('E', 'English'), ('A', 'Arabic'), ('K', 'Korean'), ('G', 'German')], max_length=1, null=True),
        ),
    ]