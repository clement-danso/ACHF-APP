# Generated by Django 2.1 on 2021-02-22 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0009_auto_20210220_0618'),
    ]

    operations = [
        migrations.CreateModel(
            name='broadcastmessagecat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Subject', models.CharField(max_length=50)),
                ('Content', models.CharField(max_length=400)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smsapp.category')),
            ],
            options={
                'verbose_name_plural': 'District Broadcast Messages',
            },
        ),
        migrations.CreateModel(
            name='broadcastmessagedis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Subject', models.CharField(max_length=50)),
                ('Content', models.CharField(max_length=400)),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smsapp.district')),
            ],
            options={
                'verbose_name_plural': 'District Broadcast Messages',
            },
        ),
        migrations.RemoveField(
            model_name='broadcastmessage',
            name='Group',
        ),
        migrations.RemoveField(
            model_name='records',
            name='group',
        ),
        migrations.AddField(
            model_name='records',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smsapp.category', verbose_name='Category'),
        ),
        migrations.DeleteModel(
            name='broadcastmessage',
        ),
    ]
