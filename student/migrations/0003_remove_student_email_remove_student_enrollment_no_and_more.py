# Generated by Django 4.0.5 on 2022-06-14 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0002_emailrecord'),
        ('student', '0002_student_assignments_assignmentsubmission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='email',
        ),
        migrations.RemoveField(
            model_name='student',
            name='enrollment_no',
        ),
        migrations.RemoveField(
            model_name='student',
            name='name',
        ),
        migrations.AddField(
            model_name='student',
            name='email_record',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='personal.emailrecord'),
        ),
    ]
