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
    comments = models.TextField('Comments', null=True)


class Decision(models.Model):
    submission = models.ForeignKey(
        'submission.Submission',
        models.CASCADE,
        related_name='decision'
    )
    accepted = models.BooleanField('Accepted', default=False)
