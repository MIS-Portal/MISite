# Generated by Django 4.0.3 on 2022-06-12 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicform', '0019_finalstudent_subcaste_student_subcaste'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='domacile',
            new_name='domicile',
        ),
    ]
