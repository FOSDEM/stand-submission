from django.core.mail import send_mail
from django.conf import settings
from .models import DURATION_CHOICES
from django.urls import reverse

_DURATION_CHOICES = {
    c[0]: c[1]
    for c in DURATION_CHOICES
}


class SubmissionMail:

    def __init__(self, submission):
        self.submission = submission

    @property
    def stands_list_message(self):
        msg = """
Hello,

A new submission has been entered in the system. It can be reviewed at {17}

For reference, this is what has been entered:

Project: {0}
Theme: {1}
Website: {2}
Source code: {3}
Requested time slot: {4}
Primary contact: {5} (<{6}>)
    Relation: {7}
Secondary contact: {8} (<{9}>)
    Relation: {10}

Description:
{11}

Social media:
{12}

Why they want to be at FOSDEM:
{13}

Showcase (digital edition):
{14}

New this year (digital edition):
{15}

Notes:
{16}

Kind regards,

The FOSDEM Stands Tool
"""
        msg = msg.format(
            self.submission.project.name,
            self.submission.project.theme.theme,
            self.submission.project.website,
            self.submission.project.source,
            _DURATION_CHOICES[self.submission.duration],
            self.submission.primary_contact.name,
            self.submission.primary_contact.email,
            self.submission.primary_reason,
            self.submission.secondary_contact.name,
            self.submission.secondary_contact.email,
            self.submission.secondary_reason,
            self.submission.project.description,
            self.submission.project.social,
            self.submission.justification,
            self.submission.digital_edition.showcase,
            self.submission.digital_edition.new_this_year,
            self.submission.notes,
            'https://stands.fosdem.org{0}?submission={1}'.format(
                reverse('review_admin:review_review_add'),
                self.submission.id
            )
        )
        return msg

    @property
    def message(self):
        msg = """
Hello,

Thank you for submitting your application for a stand at FOSDEM {0}. Your submission has been received and is currently pending review.

We hope to announce the list of accepted stands by {1}, but, depending on the volume, this deadline might be missed.

For your reference, you have submitted an application for:

Project: {2}
Theme: {3}
Requested time slot: {4}
Primary contact: {5} (<{6}>)
Secondary contact: {7} (<{8}>)


If you have any questions or remarks, please contact us at stands@fosdem.org.

Kind regards,

The FOSDEM {0} Stands Team
"""
        msg = msg.format(
            settings.EDITION,
            settings.ANNOUNCEMENT_DATE.strftime('%Y-%m-%d'),
            self.submission.project.name,
            self.submission.project.theme.theme,
            _DURATION_CHOICES[self.submission.duration],
            self.submission.primary_contact.name,
            self.submission.primary_contact.email,
            self.submission.secondary_contact.name,
            self.submission.secondary_contact.email
        )
        return msg

    def send(self):
        return [
            send_mail(
                'A new submission for FOSDEM {0}: {1}'.format(
                    settings.EDITION,
                    self.submission.project.name
                ),
                self.stands_list_message,
                'stands-tool@fosdem.org',
                [
                    'stands@fosdem.org'
                ]
            ),
            send_mail(
                'Your FOSDEM {0} submission for {1} has been received'.format(
                    settings.EDITION,
                    self.submission.project.name
                ),
                self.message,
                'stands-tool@fosdem.org',
                [
                    self.submission.primary_contact.email,
                    self.submission.secondary_contact.email
                ]
            )
        ]
