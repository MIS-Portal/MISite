# Generated by Django 4.0.6 on 2022-08-21 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basicform', '0030_alter_deletedstudent_quota_alter_finalstudent_quota_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('branch_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Clss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=20)),
                ('branch_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicform.branch')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_name', models.CharField(max_length=50)),
                ('branch_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicform.branch')),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('div_name', models.CharField(max_length=20)),
                ('branch_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicform.branch')),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicform.clss')),
            ],
        ),
    ]
