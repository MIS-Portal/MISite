# Generated by Django 4.0.3 on 2022-06-08 09:10

import basicform.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicform', '0012_alter_finalstudent_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.CharField(default=basicform.models.Student.pkgen, max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]
