# Generated by Django 4.0.3 on 2022-06-12 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicform', '0023_finalstudent_reg_no_alter_finalstudent_cap_round_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finalstudent',
            name='date_of_birth',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='finalstudent',
            name='passing_year',
            field=models.CharField(max_length=100),
        ),
    ]
