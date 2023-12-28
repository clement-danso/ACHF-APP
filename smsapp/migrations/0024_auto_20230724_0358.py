# Generated by Django 2.1 on 2023-07-24 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0023_auto_20230724_0344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='broadcastmessagecat',
            name='theme',
        ),
        migrations.AddField(
            model_name='broadcastmessagecat',
            name='theme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smsapp.theme'),
        ),
    ]
