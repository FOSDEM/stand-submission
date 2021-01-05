from django.core.mail import send_mail
from review.models import AcceptedMail
from submission.models import FOSDEMEdition
from django.conf import settings


class AcceptedSubmissionMailer:

    def __init__(self, submission):
        self.submission = submission
        self.edition = FOSDEMEdition.objects.get(year=settings.EDITION)
        self.stored_msg = AcceptedMail.objects.get(edition=self.edition)

    @property
    def msg(self):
        msg = """Hello team behind {0},

Your submission for a stand at FOSDEM {1} has been accepted.

{2}

We hope to see you at FOSDEM!

Kind regards,

The FOSDEM Stands Team
""".format(
            self.submission.project.name,
            self.edition.year,
            self.stored_msg.contents
        )
        return msg

    def send(self):
        return [
            send_mail(
                'Your FOSDEM {0} submission for {1} has been accepted'.format(
                    self.edition.year,
                    self.submission.project.name
                ),
                self.msg,
                'stands-tool@fosdem.org',
                [
                    self.submission.primary_contact.email,
                    self.submission.secondary_contact.email
                ]
            )
        ]
