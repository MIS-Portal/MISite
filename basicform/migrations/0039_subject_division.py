# Generated by Django 4.0.6 on 2022-08-22 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basicform', '0038_remove_faculty_branch_faculty_branch_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='division',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicform.division'),
        ),
    ]
