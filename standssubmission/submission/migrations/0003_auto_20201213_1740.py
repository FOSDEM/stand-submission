# Generated by Django 3.1.4 on 2020-12-13 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0002_auto_20201030_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='notes',
            field=models.TextField(blank=True, default='', verbose_name='Comments'),
        ),
    ]
