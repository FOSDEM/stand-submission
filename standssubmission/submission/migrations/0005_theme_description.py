# Generated by Django 3.1.4 on 2021-01-03 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0004_auto_20201227_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='description',
            field=models.TextField(null=True, verbose_name='Theme description'),
        ),
    ]
