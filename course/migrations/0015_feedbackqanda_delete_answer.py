# Generated by Django 4.0.5 on 2022-07-07 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0014_remove_feedback_questions_remove_question_answer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackQAndA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('answer', models.CharField(blank=True, max_length=255)),
                ('feedback', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.feedback')),
            ],
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
    ]
