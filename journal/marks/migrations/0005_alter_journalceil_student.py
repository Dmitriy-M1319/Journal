# Generated by Django 4.1.7 on 2023-05-11 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_platoon_year_alter_studentprofile_group_number_and_more'),
        ('marks', '0004_alter_journalceil_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalceil',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.studentprofile'),
        ),
    ]
