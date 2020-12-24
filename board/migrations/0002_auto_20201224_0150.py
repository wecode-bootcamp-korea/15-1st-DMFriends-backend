# Generated by Django 3.1.4 on 2020-12-23 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='writer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.member'),
        ),
        migrations.AddField(
            model_name='boardimage',
            name='board',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='board.board'),
        ),
        migrations.AddField(
            model_name='board',
            name='board_comment',
            field=models.ManyToManyField(through='board.Comment', to='user.Member'),
        ),
    ]
