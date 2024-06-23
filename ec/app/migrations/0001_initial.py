# Generated by Django 5.0 on 2023-12-16 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=500)),
                ('language', models.CharField(max_length=200)),
                ('enrolled', models.IntegerField()),
                ('url', models.URLField(max_length=1000)),
                ('level', models.CharField(max_length=300)),
                ('total_hours', models.DecimalField(decimal_places=2, max_digits=10)),
                ('type', models.CharField(max_length=500)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('syllabus', models.TextField()),
                ('date_modified', models.DateField()),
                ('certificated', models.BooleanField()),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('organization', models.CharField(max_length=255)),
                ('numberofcourse', models.IntegerField()),
                ('Field', models.CharField(max_length=255)),
                ('rating', models.DecimalField(decimal_places=2, max_digits=2)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Profile_Picture', models.ImageField(upload_to='PPimages')),
                ('Email', models.CharField(max_length=100)),
                ('Password', models.CharField(max_length=10)),
                ('Name', models.CharField(max_length=100)),
            ],
        ),
    ]