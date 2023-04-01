# Generated by Django 4.1.7 on 2023-04-01 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('hours_count', models.IntegerField()),
                ('form', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'subjects',
            },
        ),
        migrations.CreateModel(
            name='SubjectClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_date', models.DateTimeField()),
                ('theme_number', models.IntegerField()),
                ('theme_name', models.CharField(max_length=255)),
                ('class_number', models.IntegerField()),
                ('class_name', models.CharField(max_length=255)),
                ('class_type', models.CharField(max_length=30)),
                ('classroom', models.IntegerField()),
            ],
            options={
                'db_table': 'subject_classes',
            },
        ),
    ]
