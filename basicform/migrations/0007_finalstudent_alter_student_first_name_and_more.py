# Generated by Django 4.0.3 on 2022-05-08 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicform', '0006_alter_student_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinalStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('age', models.IntegerField(default=12)),
                ('date_of_birth', models.DateField(auto_now_add=True)),
                ('telephone', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(default='hi', max_length=200),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(default='chika', max_length=200),
        ),
        migrations.AlterField(
            model_name='student',
            name='telephone',
            field=models.CharField(default='12434', max_length=10),
        ),
    ]
