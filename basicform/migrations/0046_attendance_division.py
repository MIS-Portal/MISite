# Generated by Django 4.0.6 on 2022-10-24 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basicform', '0045_alter_attendance_reg_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='division',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='basicform.division'),
            preserve_default=False,
        ),
    ]
