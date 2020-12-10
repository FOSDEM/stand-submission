from django.core.mail import send_mail
from django.conf import settings
from .models import DURATION_CHOICES


_DURATION_CHOICES = {
    c[0]: c[1]
    for c in DURATION_CHOICES
}


class SubmissionMail:

    def __init__(self, submission):
        self.submission = submission

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
        return send_mail(
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
