# Generated by Django 4.0.6 on 2022-10-22 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicform', '0042_timetable_attendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timetable',
            name='subject',
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
        migrations.DeleteModel(
            name='TimeTable',
        ),
    ]
