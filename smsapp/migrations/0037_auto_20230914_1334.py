# Generated by Django 2.1 on 2023-09-14 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0036_auto_20230914_1307'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='delivery',
            options={'verbose_name_plural': 'Delmodels.FloatField()iveries'},
        ),
        migrations.AlterField(
            model_name='delivery',
            name='answer_period',
            field=models.FloatField(blank=True, max_length=50, null=True),
        ),
    ]
