# Generated by Django 3.1.4 on 2020-12-20 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20201220_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='nickname',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='password',
            field=models.CharField(max_length=200, null=True),
        ),
    ]