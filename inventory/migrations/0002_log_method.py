# Generated by Django 4.2.1 on 2023-05-24 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='method',
            field=models.CharField(default='add', max_length=40),
            preserve_default=False,
        ),
    ]