# Generated by Django 4.0.3 on 2022-06-12 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicform', '0017_rename_jee_percentile_finalstudent_jee_main_percentile_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finalstudent',
            name='SSC_board_marks',
        ),
        migrations.RemoveField(
            model_name='student',
            name='SSC_board_marks',
        ),
    ]
