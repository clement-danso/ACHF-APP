# Generated by Django 2.1 on 2022-03-04 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0016_auto_20220304_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='records',
            name='Title',
            field=models.CharField(blank=True, choices=[('Mr.', 'Mr.'), ('Mrs.', 'Mrs.'), ('Miss.', 'Miss'), ('Dr.', 'Dr.')], default='Mr.', max_length=11, null=True),
        ),
    ]
