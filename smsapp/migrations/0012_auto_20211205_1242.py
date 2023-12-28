# Generated by Django 2.1 on 2021-12-05 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0011_auto_20210314_1143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='broadcastmessagecat',
            name='category',
        ),
        migrations.AddField(
            model_name='broadcastmessagecat',
            name='category',
            field=models.ManyToManyField(to='smsapp.category'),
        ),
        migrations.AlterField(
            model_name='records',
            name='Mobile1',
            field=models.CharField(blank=True, max_length=10, verbose_name='2nd Mobile'),
        ),
        migrations.AlterField(
            model_name='records',
            name='PersonalEmail',
            field=models.CharField(blank=True, max_length=50, verbose_name='Personal Email'),
        ),
    ]
