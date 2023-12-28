# Generated by Django 2.1 on 2023-07-02 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0018_audiofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiofile',
            name='description',
            field=models.TextField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='audiofile',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
