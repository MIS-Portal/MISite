# Generated by Django 4.0.6 on 2022-10-24 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicform', '0050_alter_attendance_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='subject',
            field=models.CharField(max_length=20),
        ),
    ]
