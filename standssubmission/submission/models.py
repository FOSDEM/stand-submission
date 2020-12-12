from django.db import models

# Create your models here.

DURATION_CHOICES = [
    ('ALL', 'Entire conference'),
    ('SAT', 'Saturday'),
    ('SUN', 'Sunday')
]


class Submission(models.Model):
    fosdem_edition = models.CharField('FOSDEM edition', max_length=5)
    project = models.ForeignKey(
        'Project',
        models.CASCADE
    )
    justification = models.TextField('Justification')
    duration = models.CharField(
        'Duration',
        max_length=3,
        choices=DURATION_CHOICES,
        default='ALL'
    )
    primary_contact = models.ForeignKey(
        'Contact',
        models.CASCADE,
        related_name='primary_contact'
    )
    primary_reason = models.TextField('Primary contact relation to project')
    secondary_contact = models.ForeignKey(
        'Contact',
        models.CASCADE,
        related_name='secondary_contact'
    )
    secondary_reason = models.TextField('Secondary contact relation to project')
    notes = models.TextField('Comments', null=True)
    late_submission = models.BooleanField('Late submission', default=False)
    submission_date = models.DateTimeField('Submission date')
    submission_for_digital_edition = models.BooleanField('Digital edition', default=False)
    digital_edition = models.ForeignKey(
        'DigitalEdition',
        models.SET_NULL,
        null=True
    )

    def __str__(self):
        return '{0} submission for {1}'.format(self.fosdem_edition, self.project.name)


class Project(models.Model):
    name = models.CharField('Name', max_length=1024)
    description = models.TextField('Description')
    website = models.CharField('Website', max_length=1024)
    source = models.CharField('Source code location', max_length=1024)
    social = models.TextField('Social media links')
    theme = models.ForeignKey(
        'Theme',
        models.CASCADE
    )

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField('Name', max_length=1024)
    email = models.EmailField('E-mail address')

    def __str__(self):
        return self.name


class Theme(models.Model):
    theme = models.CharField('Theme', max_length=1024)

    def __str__(self):
        return self.theme


class DigitalEdition(models.Model):
    showcase = models.TextField('Showcase')
    new_this_year = models.TextField('What\'s new this year')

    def __str__(self):
        try:
            return 'Digital submission for {0}'.format(self.submission_set.all()[0].project.name)
        except Exception as e:
            return str(self.id)
