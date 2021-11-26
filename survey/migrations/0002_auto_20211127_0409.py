# Generated by Django 3.2.7 on 2021-11-26 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applier',
            name='is_applied',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='applier',
            name='apply_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
