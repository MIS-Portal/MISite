# Generated by Django 4.0.6 on 2022-10-24 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicform', '0046_attendance_division'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='division',
        ),
    ]
