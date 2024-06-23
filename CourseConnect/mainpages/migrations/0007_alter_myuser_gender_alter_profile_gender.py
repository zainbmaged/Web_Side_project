# Generated by Django 5.0.2 on 2024-03-18 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpages', '0006_rename_user_myuser_alter_like_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1),
        ),
    ]