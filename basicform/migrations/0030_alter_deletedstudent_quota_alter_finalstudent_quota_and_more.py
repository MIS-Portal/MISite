# Generated by Django 4.0.6 on 2022-08-04 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicform', '0029_alter_finalstudent_reg_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deletedstudent',
            name='quota',
            field=models.CharField(choices=[('CAP', 'CAP'), ('institute', 'insti. lvl'), ('pio', 'pio,J&K,J&kSSS'), ('NEUT', 'NEUT'), ('OCI', 'OCI'), ('FN', 'FN'), ('CIWC', 'CIWC'), ('TFWS', 'TFWS'), ('EWS', 'EWS'), ('DEF', 'DEF')], default='institute', max_length=20),
        ),
        migrations.AlterField(
            model_name='finalstudent',
            name='quota',
            field=models.CharField(choices=[('CAP', 'CAP'), ('institute', 'insti. lvl'), ('pio', 'pio,J&K,J&kSSS'), ('NEUT', 'NEUT'), ('OCI', 'OCI'), ('FN', 'FN'), ('CIWC', 'CIWC'), ('TFWS', 'TFWS'), ('EWS', 'EWS'), ('DEF', 'DEF')], default='institute', max_length=20),
        ),
        migrations.AlterField(
            model_name='student',
            name='quota',
            field=models.CharField(choices=[('CAP', 'CAP'), ('institute', 'insti. lvl'), ('pio', 'pio,J&K,J&kSSS'), ('NEUT', 'NEUT'), ('OCI', 'OCI'), ('FN', 'FN'), ('CIWC', 'CIWC'), ('TFWS', 'TFWS'), ('EWS', 'EWS'), ('DEF', 'DEF')], default='institute', max_length=20),
        ),
    ]
