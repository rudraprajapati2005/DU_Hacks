# Generated by Django 4.2.19 on 2025-02-22 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClassHubApp', '0010_attendance_alter_student_password_delete_attendence_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('student_id', models.CharField(max_length=20, unique=True)),
                ('semester', models.IntegerField()),
                ('year', models.IntegerField()),
                ('branch', models.CharField(max_length=50)),
                ('classroom_id', models.CharField(max_length=20)),
            ],
        ),
    ]
