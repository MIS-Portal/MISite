# Generated by Django 4.0.5 on 2022-07-03 07:13

import basicform.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicform', '0025_alter_student_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.CharField(default=basicform.models.Student.pkgen, max_length=28, primary_key=True, serialize=False, unique=True),
        ),
    ]
