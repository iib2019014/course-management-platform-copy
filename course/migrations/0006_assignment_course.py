# Generated by Django 4.0.5 on 2022-06-08 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0001_initial'),
        ('course', '0005_assignment_alter_coursematerial_material_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='personal.course'),
        ),
    ]
