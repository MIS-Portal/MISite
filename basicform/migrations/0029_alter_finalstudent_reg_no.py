# Generated by Django 4.0.6 on 2022-07-23 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicform', '0028_deletedstudent_alter_finalstudent_reg_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finalstudent',
            name='reg_no',
            field=models.CharField(default='NULL', max_length=20, unique=True),
        ),
    ]
