# Generated by Django 3.2.7 on 2021-12-02 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_auto_20211202_2355'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='required',
            field=models.BooleanField(default=False),
        ),
    ]
