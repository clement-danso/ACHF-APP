# Generated by Django 2.1 on 2021-03-14 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0010_auto_20210222_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bmc',
            name='bmcName',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='category',
            name='catName',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='district',
            name='districtName',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='grade',
            name='grade',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='group',
            name='groupName',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='records',
            name='EmpNumber',
            field=models.CharField(max_length=15, primary_key=True, serialize=False, verbose_name='Employment Number'),
        ),
        migrations.AlterField(
            model_name='region',
            name='regionName',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='subdistrict',
            name='subdistrictName',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='unit',
            name='unit',
            field=models.CharField(max_length=100),
        ),
    ]
