# Generated by Django 4.0.5 on 2022-07-06 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0004_course_highest_rate_course_rate_1_course_rate_2_and_more'),
        ('course', '0011_question_feedback_questions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='personal.course')),
            ],
        ),
    ]
