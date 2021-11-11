# Generated by Django 3.2.9 on 2021-11-10 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Admin'), (2, 'Accountant'), (3, 'Manager'), (4, 'Employee')], default=4),
        ),
    ]