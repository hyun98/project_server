# Generated by Django 3.2.7 on 2021-09-15 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FAQs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='FAQs.question'),
        ),
    ]