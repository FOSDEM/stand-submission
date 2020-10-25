# Generated by Django 3.1.2 on 2020-10-25 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail address')),
            ],
        ),
        migrations.CreateModel(
            name='DigitalEdition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('showcase', models.TextField(verbose_name='Showcase')),
                ('new_this_year', models.TextField(verbose_name="What's new this year")),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('website', models.CharField(max_length=1024, verbose_name='Website')),
                ('source', models.CharField(max_length=1024, verbose_name='Source code location')),
                ('social', models.TextField(verbose_name='Social media links')),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=1024, verbose_name='Theme')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fosdem_edition', models.CharField(max_length=5, verbose_name='FOSDEM edition')),
                ('justification', models.TextField(verbose_name='Justification')),
                ('duration', models.CharField(choices=[('ALL', 'Entire conference'), ('SAT', 'Saturday'), ('SUN', 'Sunday')], default='ALL', max_length=3, verbose_name='Duration')),
                ('primary_reason', models.TextField(verbose_name='Primary contact relation to project')),
                ('secondary_reason', models.TextField(verbose_name='Secondary contact relation to project')),
                ('notes', models.TextField(verbose_name='Comments')),
                ('late_submission', models.BooleanField(default=False, verbose_name='Late submission')),
                ('submission_date', models.DateTimeField(verbose_name='Submission date')),
                ('submission_for_digital_edition', models.BooleanField(default=False, verbose_name='Digital edition')),
                ('digital_edition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='submission.digitaledition')),
                ('primary_contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_contact', to='submission.contact')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='submission.project')),
                ('secondary_contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secondary_contact', to='submission.contact')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='submission.theme'),
        ),
    ]
