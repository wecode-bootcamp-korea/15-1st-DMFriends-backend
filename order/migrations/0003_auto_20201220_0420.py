# Generated by Django 3.1.4 on 2020-12-20 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20201217_1533'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='kakao_pay_id',
            new_name='kakao_pay',
        ),
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
