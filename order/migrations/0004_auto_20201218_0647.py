# Generated by Django 3.1.4 on 2020-12-18 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20201218_0644'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='payments_status',
            new_name='payment_status',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='payments_type',
            new_name='payment_type',
        ),
    ]