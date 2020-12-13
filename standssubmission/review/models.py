from django.db import models
from django.conf import settings

# Create your models here.


class Review(models.Model):
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='reviews'
    )
    submission = models.ForeignKey(
        'submission.Submission',
        models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        'Score',
        default=0
    )
    comments = models.TextField('Comments', default='', blank=True)

    def __str__(self):
        reviewer = self.reviewer.username
        if self.reviewer.first_name and self.reviewer.last_name:
            reviewer = '{0} {1}'.format(self.reviewer.first_name, self.reviewer.last_name)
        return 'Review by {0} for {1}'.format(reviewer, self.submission.__str__())

    def current_decision(self):
        return self.submission.decision.accepted


class Decision(models.Model):
    submission = models.OneToOneField(
        'submission.Submission',
        models.CASCADE,
        related_name='decision'
    )
    accepted = models.BooleanField('Accepted', default=False)

    def __str__(self):
        accepted = 'accepted'
        if not self.accepted:
            accepted = 'not accepted'
        return '{0}: {1}'.format(
            self.submission.__str__(),
            accepted
        )
