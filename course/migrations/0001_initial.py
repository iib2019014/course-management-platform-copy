# Generated by Django 4.0.5 on 2022-06-08 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_type', models.CharField(choices=[('Link', 'Link'), ('File', 'File')], max_length=255)),
                ('material_link', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]