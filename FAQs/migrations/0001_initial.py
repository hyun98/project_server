# Generated by Django 3.2.7 on 2021-10-09 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(null=True)),
                ('order', models.PositiveIntegerField(default=0, null=True)),
            ],
            options={
                'verbose_name': '자주 묻는 질문',
                'verbose_name_plural': '자주 묻는 질문들',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(null=True)),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='FAQs.question')),
            ],
        ),
    ]
