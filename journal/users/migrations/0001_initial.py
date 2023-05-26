# Generated by Django 4.1.6 on 2023-05-14 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseDirection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.IntegerField()),
                ('direction', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'course_directions',
            },
        ),
        migrations.CreateModel(
            name='Platoon',
            fields=[
                ('platoon_number', models.IntegerField(primary_key=True, serialize=False)),
                ('year', models.IntegerField(null=True)),
                ('status', models.CharField(max_length=15)),
                ('study_day', models.IntegerField()),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.coursedirection')),
            ],
            options={
                'db_table': 'platoons',
            },
        ),
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=50, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('patronymic', models.CharField(max_length=40, null=True)),
                ('military_post', models.CharField(max_length=255, null=True)),
                ('military_rank', models.CharField(max_length=20)),
                ('cycle', models.CharField(max_length=255)),
                ('teacher_role', models.IntegerField(null=True)),
                ('status', models.CharField(max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'teachers',
            },
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=50, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('patronymic', models.CharField(max_length=40, null=True)),
                ('military_post', models.CharField(max_length=255, null=True)),
                ('department', models.CharField(max_length=255)),
                ('group_number', models.IntegerField(null=True)),
                ('active', models.CharField(max_length=30)),
                ('platoon', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.platoon')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'students',
            },
        ),
        migrations.AddField(
            model_name='platoon',
            name='tutor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='users.teacherprofile'),
        ),
    ]
