# Generated by Django 3.1.4 on 2020-12-20 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20201220_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='nickname',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='member',
            name='password',
            field=models.CharField(default='', max_length=200),
        ),
    ]
